from sqlalchemy.orm import Session
from app.models.order import Order, PaymentType
from app.models.invoice import Invoice
from typing import Dict, Any, Optional
from datetime import datetime
import logging

# Set up logging
logger = logging.getLogger(__name__)

class PaymentService:
    """Service class for handling payment-related operations"""
    
    # Supported payment methods and their configurations
    PAYMENT_METHODS = {
        "cash": {
            "name": "Cash",
            "requires_processing": False,
            "instant_confirmation": True
        },
        "card": {
            "name": "Credit/Debit Card",
            "requires_processing": True,
            "instant_confirmation": False
        },
        "qr": {
            "name": "QR Code Payment",
            "requires_processing": True,
            "instant_confirmation": False
        },
        "e_wallet": {
            "name": "Electronic Wallet",
            "requires_processing": True,
            "instant_confirmation": False
        },
        "gift_card": {
            "name": "Gift Card",
            "requires_processing": True,
            "instant_confirmation": False
        }
    }
    
    @staticmethod
    def validate_payment_type(payment_type: str) -> bool:
        """Validate if the payment type is supported"""
        return payment_type in PaymentService.PAYMENT_METHODS
    
    @staticmethod
    def get_payment_method_info(payment_type: str) -> Dict[str, Any]:
        """Get information about a payment method"""
        return PaymentService.PAYMENT_METHODS.get(payment_type, {})
    
    @staticmethod
    def process_payment(db: Session, order_id: int, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a payment for an order
        
        Args:
            db: Database session
            order_id: ID of the order to process payment for
            payment_data: Payment information (method, amount, etc.)
            
        Returns:
            Dict containing payment result information
        """
        try:
            # Get the order
            order = db.query(Order).filter(Order.id == order_id).first()
            if not order:
                return {
                    "success": False,
                    "error": "Order not found"
                }
            
            # Validate payment type
            payment_type = payment_data.get("payment_type", "cash")
            if not PaymentService.validate_payment_type(payment_type):
                return {
                    "success": False,
                    "error": f"Invalid payment type: {payment_type}"
                }
            
            # Get payment method info
            payment_method = PaymentService.PAYMENT_METHODS[payment_type]
            
            # Check if amount matches order total
            amount = payment_data.get("amount", 0)
            if amount != order.total:
                return {
                    "success": False,
                    "error": "Payment amount does not match order total"
                }
            
            # Process payment based on method
            if payment_method["requires_processing"]:
                # For methods that require processing (card, QR, e-wallet, gift card)
                # In a real implementation, this would connect to payment processors
                processing_result = PaymentService._simulate_payment_processing(payment_data)
                if not processing_result["success"]:
                    return processing_result
                
                # Update order with payment reference if provided
                payment_reference = processing_result.get("reference")
                if payment_reference:
                    order.payment_reference = payment_reference
            
            # Update order payment type and status
            order.payment_type = payment_type
            order.payment_status = "completed"
            order.paid_at = datetime.utcnow()
            
            # Commit changes
            db.commit()
            db.refresh(order)
            
            # Create invoice if it doesn't exist
            invoice = db.query(Invoice).filter(Invoice.order_id == order_id).first()
            if not invoice:
                from app.services.invoice_service import invoice_service
                try:
                    invoice = invoice_service.create_invoice_from_order(db, order_id)
                except Exception as e:
                    logger.error(f"Failed to create invoice for order {order_id}: {str(e)}")
            
            return {
                "success": True,
                "order_id": order_id,
                "payment_type": payment_type,
                "amount": amount,
                "timestamp": datetime.utcnow(),
                "invoice_id": invoice.id if invoice else None
            }
            
        except Exception as e:
            logger.error(f"Error processing payment for order {order_id}: {str(e)}")
            db.rollback()
            return {
                "success": False,
                "error": f"Payment processing failed: {str(e)}"
            }
    
    @staticmethod
    def _simulate_payment_processing(payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulate payment processing (in a real system, this would connect to payment gateways)
        
        Args:
            payment_data: Payment information
            
        Returns:
            Dict containing processing result
        """
        # In a real implementation, this would:
        # 1. Connect to payment processor API
        # 2. Send payment details
        # 3. Wait for response
        # 4. Handle success/failure
        
        # For simulation, we'll just return success
        return {
            "success": True,
            "reference": f"txn_{int(datetime.utcnow().timestamp())}",
            "processed_at": datetime.utcnow()
        }
    
    @staticmethod
    def refund_payment(db: Session, order_id: int, refund_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a refund for a paid order
        
        Args:
            db: Database session
            order_id: ID of the order to refund
            refund_data: Refund information
            
        Returns:
            Dict containing refund result information
        """
        try:
            # Get the order
            order = db.query(Order).filter(Order.id == order_id).first()
            if not order:
                return {
                    "success": False,
                    "error": "Order not found"
                }
            
            # Check if order was paid
            if not order.payment_status or order.payment_status != "completed":
                return {
                    "success": False,
                    "error": "Order has not been paid"
                }
            
            # Check if a refund has already been processed
            if hasattr(order, 'refund_status') and order.refund_status == "completed":
                return {
                    "success": False,
                    "error": "Order has already been refunded"
                }
            
            # Process refund based on payment method
            payment_type = order.payment_type
            payment_method = PaymentService.PAYMENT_METHODS.get(payment_type, {})
            
            if payment_method.get("requires_processing", False):
                # For methods that require processing, simulate refund
                refund_result = PaymentService._simulate_refund_processing(order, refund_data)
                if not refund_result["success"]:
                    return refund_result
            
            # Update order with refund information
            order.refund_status = "completed"
            order.refunded_at = datetime.utcnow()
            
            # Optionally update invoice
            invoice = db.query(Invoice).filter(Invoice.order_id == order_id).first()
            if invoice:
                invoice.refund_status = "completed"
                invoice.refunded_at = datetime.utcnow()
            
            # Commit changes
            db.commit()
            db.refresh(order)
            
            return {
                "success": True,
                "order_id": order_id,
                "payment_type": payment_type,
                "refunded_amount": order.total,
                "timestamp": datetime.utcnow(),
                "reference": f"refund_{int(datetime.utcnow().timestamp())}"
            }
            
        except Exception as e:
            logger.error(f"Error processing refund for order {order_id}: {str(e)}")
            db.rollback()
            return {
                "success": False,
                "error": f"Refund processing failed: {str(e)}"
            }
    
    @staticmethod
    def _simulate_refund_processing(order: Order, refund_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulate refund processing (in a real system, this would connect to payment gateways)
        
        Args:
            order: Order to refund
            refund_data: Refund information
            
        Returns:
            Dict containing refund processing result
        """
        # In a real implementation, this would:
        # 1. Connect to payment processor API
        # 2. Send refund request
        # 3. Wait for response
        # 4. Handle success/failure
        
        # For simulation, we'll just return success
        return {
            "success": True,
            "reference": f"refund_{int(datetime.utcnow().timestamp())}",
            "processed_at": datetime.utcnow()
        }
    
    @staticmethod
    def get_payment_summary(db: Session, start_date: Optional[datetime] = None, 
                           end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Get payment summary statistics
        
        Args:
            db: Database session
            start_date: Start date for filtering (optional)
            end_date: End date for filtering (optional)
            
        Returns:
            Dict containing payment summary information
        """
        try:
            # Build query for orders
            query = db.query(Order)
            
            # Apply date filters if provided
            if start_date:
                query = query.filter(Order.paid_at >= start_date)
            if end_date:
                query = query.filter(Order.paid_at <= end_date)
            
            # Get all paid orders
            paid_orders = query.filter(Order.payment_status == "completed").all()
            
            # Calculate summary statistics
            total_revenue = sum(order.total for order in paid_orders)
            
            # Group by payment type
            payment_type_breakdown = {}
            for order in paid_orders:
                payment_type = order.payment_type if order.payment_type else "cash"
                if payment_type not in payment_type_breakdown:
                    payment_type_breakdown[payment_type] = {
                        "count": 0,
                        "amount": 0.0
                    }
                payment_type_breakdown[payment_type]["count"] += 1
                payment_type_breakdown[payment_type]["amount"] += order.total
            
            return {
                "success": True,
                "total_revenue": total_revenue,
                "total_transactions": len(paid_orders),
                "payment_type_breakdown": payment_type_breakdown,
                "period": {
                    "start_date": start_date.isoformat() if start_date else None,
                    "end_date": end_date.isoformat() if end_date else None
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating payment summary: {str(e)}")
            return {
                "success": False,
                "error": f"Failed to generate payment summary: {str(e)}"
            }

# Create a singleton instance
payment_service = PaymentService()