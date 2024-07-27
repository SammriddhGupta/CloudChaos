// PricingPage.js
import React from "react";
import backgroundImage from "./background.jpg";
import pricingImage from "../PaymentModel.png"; 
import paymentImage from "../Payment.png"; 

function PricingPage() {
  return (

    <div
      className="content"
      style={{
        backgroundImage: `url(${backgroundImage})`,
        backgroundSize: "cover",
        backgroundRepeat: "no-repeat",
        backgroundAttachment: "fixed",
        backgroundPosition: "center",
        minHeight: "10vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <img
        src={pricingImage}
        alt="Pricing"
        style={{
          maxWidth: "70%",
          height: "auto",
        }}
      />
      <img
        src={paymentImage}
        alt="Payment"
        style={{
          maxWidth: "30%",
          height: "auto",
        }}
      />
    </div>
  );
}

export default PricingPage;
