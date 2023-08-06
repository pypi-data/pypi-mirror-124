from .base import APIEndpoint

from banqup_uc.models.intakeresponses import IntakeV3Response
from banqup_uc.helpers import getFilename

class PurchaseInvoiceMethods(APIEndpoint):

    def __init__(self, api):
        super(PurchaseInvoiceMethods, self).__init__(api, 'purchase-invoices')
    
    def upload(self, filePath):

        url = self.endpoint
        data = { 'client_id' : self.api.enterpriseId }

        fileBinary = open(filePath, 'rb')
        
        files = [('file', ('file.pdf', fileBinary, 'application/pdf'))]

        status, headers, respJson = self.api.post(url, data, files=files)
        
        if status != 200: return IntakeV3Response().parseError(respJson)

        return IntakeV3Response().parse(respJson)