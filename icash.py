import requests
import json
from datetime import datetime
from dateutil.parser import parse
from time import sleep
import pandas as pd

now = datetime.now()

class iCash:

    def __init__(self):
        self.baseURL = "https://icashmerchantv2.azurewebsites.net"
        self.tokenValid = False
        self.tokenExpiry = parse("1/1/1970")
        self.accessToken = ""

    def checkToken(self):
        if now >= self.tokenExpiry:
            raise ValueError("Access Token has expired, use the iCash.login method to renew access token.")

    def login(self, username, password):
        path = "/Token"
        reqURL = self.baseURL + path

        reqHeaders = {"Content-Type": "application/x-www-form-urlencoded"}

        reqBody = {"UserName": username,
                   "Password": password,
                   "grant_type": "password"}

        print("Logging In...", end="")
        req = requests.post(reqURL, headers=reqHeaders, data=reqBody)

        if req.ok:
            self.tokenValid = True
            res = json.loads(req.text)
            self.tokenExpiry = parse(res[".expires"])
            print(f"SUCCESS\nAccess token:{res['access_token']}")
            print("_____________________________________________")
            self.accessToken = res['access_token']

        else:
            print(f"FAILED\nError {req.status_code}\n{req.text}")
            sleep(5)
            exit()


    def getBalance(self, card_no):
        path = "/api/ICashAccount/GetBalance"
        reqURL = self.baseURL + path

        reqHeaders = {"Authorization": f"Bearer {self.accessToken}"}
        reqParams = {"iCashCardNumber": card_no}

        print("Getting Balance...", end="")
        req = requests.get(reqURL, headers=reqHeaders, params=reqParams)

        if req.ok:
            res = json.loads(req.text)
            balance = res['CurrentBalance']
            print(f"SUCCESS\nBalance:{balance}")
            print("_____________________________________________")
            return balance
        else:
            print(f"FAILED\nError {req.status_code}\n{req.text}")
            sleep(5)
            exit()


    def getStatement(self, cardNo, fromDate, toDate, noRecords):
        path = "/api/ICashAccount/GetStatement"
        reqURL = self.baseURL + path

        reqHeaders = {"Authorization": f"Bearer {self.accessToken}"}

        dateFormat = "%Y-%m-%d"
        fromDate = parse(fromDate).strftime(dateFormat)
        toDate = parse(toDate).strftime(dateFormat)

        reqParams = {"iCashCardNumber": cardNo,
                     "From": fromDate,
                     "To": toDate,
                     "NumberOfRecords": noRecords}

        print("Getting Statement...", end="")
        req = requests.get(reqURL, headers=reqHeaders, params=reqParams)

        if req.ok:
            res = json.loads(req.text)
            balance = res["CurrentBalance"]
            statement = res["Statement"]
            statementDF = pd.DataFrame(res["Statement"])
            print(f"SUCCESS\nBalance:{balance}\nStatement:{statement}")
            print(statementDF)
            print("_____________________________________________")
            return balance, statement
        else:
            print(f"FAILED\nError {req.status_code}\n{req.text}")


    def transferMoney(self, toCardNo, fromCardNo, amount, msg):
        path = "/api/ICashAccount/TransferMoney"
        reqURL = self.baseURL + path

        reqHeaders = {"Content-Type": "application/x-www-form-urlencoded",
                      "Authorization": f"Bearer {self.accessToken}"}

        reqBody = {"ReseveriCashCardNumber": toCardNo,
                   "Amount": amount,
                   "Message": msg}

        reqParams = {"iCashCardNumber": fromCardNo}

        print("Sending Money...", end="")
        req = requests.post(reqURL, headers=reqHeaders, params=reqParams, data=reqBody)

        if req.ok:
            res = json.loads(req.text)
            print(f"SUCCESS\nOperation Number:{res['OperationReferenceNumber']}\nDatetime:{res['DateTime']}")
            print("_____________________________________________")
            return res['OperationReferenceNumber']
        else:
            print(f"FAILED\nError {req.status_code}\n{req.text}")
            sleep(5)
            exit()


    def GenPaymentCode(self, shopNo, amount, fromCardNo):
        path = "/api/ICashAccount/GeneratePaymentCode"
        reqURL = self.baseURL + path

        reqHeaders = {"Content-Type": "application/x-www-form-urlencoded",
                      "Authorization": f"Bearer {self.accessToken}"}

        reqBody = {"ShopNumber": shopNo,
                   "Amount": amount}

        reqParams = {"iCashCardNumber": fromCardNo}

        print("Generating Payment Code...", end="")
        req = requests.post(reqURL, headers=reqHeaders, params=reqParams, data=reqBody)

        if req.ok:
            res = json.loads(req.text)
            print(f"SUCCESS\nPayment Code:{res['PaymentCode']}\nDatetime:{res['DateTime']}")
            print("_____________________________________________")
            return res['PaymentCode']
        else:
            print(f"FAILED\nError {req.status_code}\n{req.text}")
            sleep(5)
            exit()


    def validateVoucher(self, voucherNo, voucherValue, cardNo):
        path = "/api/ICashAccount/ValidateVoucher"
        reqURL = self.baseURL + path

        reqHeaders = {"Content-Type": "application/x-www-form-urlencoded",
                      "Authorization": f"Bearer {self.accessToken}"}

        reqBody = {"Voucher": voucherNo,
                   "VoucherValue": voucherValue}

        reqParams = {"iCashCardNumber": cardNo}

        print("Validating Voucher...", end="")
        req = requests.post(reqURL, headers=reqHeaders, params=reqParams, data=reqBody)

        if req.ok:
            res = json.loads(req.text)
            print(
                f"SUCCESS\nSecret No:{res['SecretNo']}\nAmount:{res['Amount']}\nValid:{res['Valid']}\nVoucherICashNetwork:{res['VoucherICashNetwork']}\nChargeDate:{res['ChargeDate']}")
            print("_____________________________________________")
            return res['Valid']
        else:
            print(f"FAILED\nError {req.status_code}\n{req.text}")
            sleep(5)
            exit()


    def redeemVoucher(self, voucherNo, voucherValue, cardNo):
        path = "/api/ICashAccount/RedeemVoucher"
        reqURL = self.baseURL + path

        reqHeaders = {"Content-Type": "application/x-www-form-urlencoded",
                      "Authorization": f"Bearer {self.accessToken}"}

        reqBody = {"Voucher": voucherNo,
                   "VoucherValue": voucherValue}

        reqParams = {"iCashCardNumber": cardNo}

        print("Redeeming Voucher...", end="")
        req = requests.post(reqURL, headers=reqHeaders, params=reqParams, data=reqBody)

        if req.ok:
            res = json.loads(req.text)
            print(f"SUCCESS\nOperationReferenceNumber:{res['OperationReferenceNumber']}\nDateTime:{res['DateTime']}")
            print("_____________________________________________")
            return res['OperationReferenceNumber']
        else:
            print(f"FAILED\nError {req.status_code}\n{req.text}")
            sleep(5)
            exit()


    def payInvoice(self, cardNo, customerCardNo, invTotalAmnt, paymentCode, description):
        path = "/api/ICashAccount/PayInvoice"
        reqURL = self.baseURL + path

        reqHeaders = {"Content-Type": "application/x-www-form-urlencoded",
                      "Authorization": f"Bearer {self.accessToken}"}

        reqBody = {"CustomeriCashCardNumber": customerCardNo,
                   "InvoiceTotalAmount": invTotalAmnt,
                   "PaymentCode": paymentCode,
                   "Description": description}

        reqParams = {"iCashCardNumber": cardNo}

        print("Paying Invoice...", end="")
        req = requests.post(reqURL, headers=reqHeaders, params=reqParams, data=reqBody)

        if req.ok:
            res = json.loads(req.text)
            print(f"SUCCESS\nOperationReferenceNumber:{res['OperationReferenceNumber']}\nDateTime:{res['DateTime']}")
            print("_____________________________________________")
            return res['OperationReferenceNumber']
        else:
            print(f"FAILED\nError {req.status_code}\n{req.text}")
            sleep(5)
            exit()


    def getiCashCardNetworkNumber(self, iCashCardNumber):
        path = "/api/ICashAccount/GetiCashCardNetworkNumber"
        reqURL = self.baseURL + path

        reqHeaders = {"Content-Type": "application/x-www-form-urlencoded",
                      "Authorization": f"Bearer {self.accessToken}"}

        reqParams = {"iCashCardNumber": iCashCardNumber}

        print("Gettting iCash Card Network Number...", end="")
        req = requests.get(reqURL, headers=reqHeaders, params=reqParams)

        if req.ok:
            res = json.loads(req.text)
            pkgNo = res['PackageNumber']
            print(f"SUCCESS\nPackage Number:{pkgNo}")
            print("_____________________________________________")
            return pkgNo
        else:
            print(f"FAILED\nError {req.status_code}\n{req.text}")
            sleep(5)
            exit()


    def canCustomerPurchase(self, iCashCardNumber, customeriCashCardNumber, amount, generateInvoiceQR):
        path = "/api/Merchant/CanCustomerPurchase"
        reqURL = self.baseURL + path

        reqHeaders = {"Content-Type": "application/x-www-form-urlencoded",
                      "Authorization": f"Bearer {self.accessToken}"}

        reqParams = {"iCashCardNumber": iCashCardNumber}

        reqBody = {"CustomeriCashCardNumber": customeriCashCardNumber,
                   "Amount": amount,
                   "GenerateInvoiceQR": generateInvoiceQR}

        print("Checking If Customer Can Purchase...", end="")
        req = requests.post(reqURL, headers=reqHeaders, params=reqParams, data=reqBody)

        if req.ok:
            res = json.loads(req.text)
            pkgNo = res['PackageNumber']
            print(f"SUCCESS\nPackage Number:{pkgNo}")
            print("_____________________________________________")
            return pkgNo
        else:
            print(f"FAILED\nError {req.status_code}\n{req.text}")
            sleep(5)
            exit()


    def showQR(self, shopID, amount):
        path = "/api/Merchant/GeneratePaymentQR"
        reqURL = self.baseURL + path

        reqHeaders = {"Content-Type": "application/x-www-form-urlencoded",
                      "Authorization": f"Bearer {self.accessToken}"}

        reqParams = {"Amount": amount,
                     "ShopID": shopID}

        print("Getting QR Code...", end="")
        req = requests.get(reqURL, headers=reqHeaders, params=reqParams)

        if req.ok:
            res = req.content
            with open("imageToSave.png", "wb") as fh:
                fh.write(res)
            print("_____________________________________________")
        else:
            print(f"FAILED\nError {req.status_code}\n{req.text}")
            sleep(5)
            exit()


    def setNewPIN(self, cardNo, PIN, confPIN):
        path = "/api/ICashAccount/SetNewPIN"
        reqURL = self.baseURL + path

        reqHeaders = {"Content-Type": "application/x-www-form-urlencoded",
                      "Authorization": f"Bearer {self.accessToken}"}

        reqBody = {"PIN": PIN,
                   "ConfirmPIN": confPIN}

        reqParams = {"iCashCardNumber": cardNo}

        print("Setting New PIN...", end="")
        req = requests.post(reqURL, headers=reqHeaders, params=reqParams, data=reqBody)

        if req.ok:
            res = json.loads(req.text)
            print(f"SUCCESS\nIs Operation Successful?:{res['IsOperationSuccessful']}\nDateTime:{res['DateTime']}")
            print("_____________________________________________")
            return res['IsOperationSuccessful']
        else:
            print(f"FAILED\nError {req.status_code}\n{req.text}")
            sleep(5)
            exit()
'''
Example usage of iCash client
-----------------------------
iCashClient = iCash() #Initiating an instance of iCash client
iCashClient.login("example@website.com", "P@$$W0RD") #Performing login using username and password
iCashClient.getBalance(1000103943) #Getting balance of a given iCash card
iCashClient.getStatement(1000103943, "1 Jan 2021", "31 Dec 2021", "25") #Get statement of transaction history for a given date range
iCashClient.TransferMoney(1000100261,1000103943,1,"Testing Transfer Money")
iCashClient.GenPaymentCode("12","0","1000103943")
iCashClient.ValidateVoucher("57157764019253", "10","1000103943")
iCashClient.RedeemVoucher("57157764019253", "10", "1000103943")
iCashClient.PayInvoice(1000100261,1000130060, 0, 3815651, "Testing Pay Invoice")
iCashClient.getiCashCardNetworkNumber(7120111682)
iCashClient.CanCustomerPurchase(1000100261, 1000130060, 0, True)
iCashClient.ShowQR(10,5)
iCashClient.setNewPIN(1000100261, 8082, 8082)
'''
