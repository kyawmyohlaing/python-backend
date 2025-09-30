import React, { useState } from 'react';
import './PaymentMethodSelector.css';

const PaymentMethodSelector = ({ 
  selectedPaymentMethod, 
  onPaymentMethodChange,
  className = '' 
}) => {
  // Payment method options based on backend implementation
  const paymentMethods = [
    { id: 'cash', name: 'Cash', icon: '💰' },
    { id: 'card', name: 'Card', icon: '💳' },
    { id: 'qr', name: 'QR Code', icon: '📱' },
    { id: 'e_wallet', name: 'E-Wallet', icon: '💼' },
    { id: 'gift_card', name: 'Gift Card', icon: '🎁' }
  ];

  const handlePaymentMethodChange = (methodId) => {
    if (onPaymentMethodChange) {
      onPaymentMethodChange(methodId);
    }
  };

  return (
    <div className={`payment-method-selector ${className}`}>
      <h3>Payment Method</h3>
      <div className="payment-methods-grid">
        {paymentMethods.map((method) => (
          <button
            key={method.id}
            className={`payment-method-button ${
              selectedPaymentMethod === method.id ? 'selected' : ''
            }`}
            onClick={() => handlePaymentMethodChange(method.id)}
            aria-pressed={selectedPaymentMethod === method.id}
          >
            <span className="payment-icon">{method.icon}</span>
            <span className="payment-name">{method.name}</span>
          </button>
        ))}
      </div>
    </div>
  );
};

export default PaymentMethodSelector;