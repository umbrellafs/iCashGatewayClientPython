
  
# Umbrella iCash Client
This is an implementation of an Umbrella iCash cleint in Python.    
It contains the following 12 functions:    
 - [Login](#login)    
 - [Get Balance](#get-balance)    
 - [Get Statement](#get-statement)  
 - [Transfer Money](#transfer-money)  
 - [Generate Payment Code](#generate-payment-code)  
 - [Validate Voucher](#validate-voucher)  
 - [Redeem Voucher](#redeem-voucher)  
 - [Pay Invoice](#pay-invoice)  
 - [Get iCash Card Network Number](#get-icash-card-network-number)  
 - [Can Customer Purchase?](#can-customer-purchase)  
 - [Show QR Code](#show-qr-code)  
 - [Set New PIN](#set-new-pin)  

# Creating an instance of iCash Gateway Client

    iCashGatewayClient = iCash()

# Login
First thing that needs to performed is login. The `login` method required the folliwng two parameters.
 - Username
 - Password
## Example

    iCashGatewayClient.login("example@website.com", "P@$$W0RD")

## Response

    AscW3TSUI1JWetnIjjaoGYadzPyxwAHRvrsSf55ZIg3ILIlFssy2hDPsU6isSgKaybTl4BQT5Qze54-XmxUFkwoPoqrfxEzshcVLdEKlnq1bRhA1qAkSqV3xcfHjIPXdmqPpFdKcA_MBos7vazojVHF8j026DvbN2LDWlUngP48k08uIRdKvRn0SRaNaQlW3CCS6oGdIEMmM9CgXCnFhlRrEzGH8WoU2gYYcDmGfYS9wzk_QbQrEGQTiWQMThkgKOKFgwJlRiQnGxUG3JrKT1tkg4tkl0llQTayRau_cM3EkRTVzNWW2HuskIFwkUGIW_A9f5XHr3MYOy-wTV9Wo2lyqBqSwCTxgELXJRRUh1-QKEqsvC3afdVHjhXeZE4u9n4LWYJeWry1LSYKbCmu2MmiF3eSSnn_0i7b6gEciqVjZRYf_qkinw1FWNiFhOajHbAX-H1fc9XW32VUsmFcAdVx-Wrrl4b11zRy5OdT7rVRgEnz1B2YxGvrZH9H2Lg2E

# Get Balance
This function returns the current balance of a given iCash card number.    
The `getBalance` function requires three parameters:     
 - iCash Card Number    
  
The iCash card number **MUST** be linked to the account used in the `login` function, otherwise the request will be denied.    
## Example

    iCashGatewayClient.getBalance(iCashCarNo)

## Response

    Insert Resposne Here


# Get Statement
This function returns the current balance of a given iCash card number as well as a statement containing a given number of the most recent transactions for a specified date range.  
The function reuiresthe following 6 parameters:   
 - iCash Card Number      
 - Start Date    
 - End Date    
 - Number of records
  
The iCash card number **MUST** be linked to the account used in the `login` function, otherwise the request will be denied.    
  
## Example

    iCashGatewayClient.getStatement(iCashCarNo, startDate, endDate, noRecords)

## Response

    Insert Resposne Here

# Transfer Money
This function is used to transfer funds from one iCash card to another. It requires 6 parameters:
 - Recipient (To) iCash Card Number
 - Source (From) iCash Card Number
 - Amount
 - Message (optional)
  
## Example

    iCashGatewayClient.transferMoney(toCardNo, fromCardNo, amount, msg)

## Response

    Insert Resposne Here

If operation successful, the function will return an `OperationReferenceNumber`  
  
The iCash card number **MUST** be linked to the account used in the `login` function, otherwise the request will be denied.    
  
# Generate Payment Code
This function generates a payment code for a given amount that will be paid to a given shop number.  
The function requires 5 parameters:
 - Shop Number  
 - Amount  
 - iCash Card Number  
  
## Example

    iCashGatewayClient.GenPaymentCode(shopNo, amount, CardNo)

## Response

    Insert Resposne Here
If successful, the function will return a 7-digit payment code.  
  
# Validate Voucher
This function checks whether a given voucher is valid and redeemable by a given iCash card number.  
The function requires 5 parameters:
 - Voucher Secret Number  
 - Voucher Value  
 - iCash Card Number  

## Example

    iCashGatewayClient.validateVoucher(voucherNo, voucherValue, cardNo)

## Response

    Insert Resposne Here
# Redeem Voucher
This function redeems a given valid voucher to a given iCash card number.  
The function requires 5 parameters:     
 - Voucher Secret Number  
 - Voucher Value  
 - iCash Card Number  
  
## Example

    iCashGatewayClient.redeemVoucher(voucherNo, voucherValue, cardNo)

## Response

    Insert Resposne Here
If successful, the function will return an `OperationReferenceNumber`  
  
# Pay Invoice
This function is used to pay an invoice with a given amount from a customer's iCash card number to a merchant's iCash card number.  
The function requires the following 7 parameters:     
 - Merchant iCash Card Number  
 - Customer iCash Card Number  
 - Amount  
 - Payment Code - generated from the [Generate Payment Code](#generate-payment-code) function  
 - Description (optional)  
  
## Example

    iCashGatewayClient.payInvoice(cardNo, customerCardNo, invTotalAmnt, paymentCode, description)

## Response

    Insert Resposne Here

# Get iCash Card Network Number
This function returns the network number for a given iCash card number.  
The function requires three parameters:
 - iCash Card Number 

## Example

    iCashGatewayClient.getiCashCardNetworkNumber(CardNo)

## Response

    Insert Resposne Here

# Can Customer Purchase?
This function determines whether a customer can purchase a given amount from a given merchant.  
The function requires the following 6 parameters:
 - Merchant iCash Card Number  
 - Customer iCash Card Number  
 - Amount  
 - Generate Invoice QR (Boolean) - if `True`, the function will also return the invoice QR code for the given amount and merchant shop number.  
  
## Example

    iCashGatewayClient.canCustomerPurchase(iCashCardNumber, customeriCashCardNo, amount, generateInvoiceQR)

## Response

    Insert Resposne Here

# Show QR Code
This function returns the invoice QR code for any given amount and shop number.  
The function requires the following 4 parameters:
 - Shop Number  
 - Amount  

## Example

    iCashGatewayClient.showQR(shopID, amount)


## Response

    Insert Resposne Here

# Set New PIN  
This function sets a new PIN for a given iCash card number.  
The function requires the following 4 parameters:   
 - iCash Card Number  
 - New PIN  
 - Repeat New PIN  

## Example

    iCashGatewayClient.setNewPIN(cardNo, PIN, confPIN)

## Response

    Insert Resposne Here

If successful, the function will return `True`