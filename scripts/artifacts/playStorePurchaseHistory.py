import datetime
import json
import os

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows

def get_playStorePurchaseHistory(files_found, report_folder, seeker, wrap_text):
    
    for file_found in files_found:
        file_found = str(file_found)
        if not os.path.basename(file_found) == 'Purchase History.json': # skip -journal and other files
            continue

        with open(file_found, "r") as f:
            data = json.loads(f.read())
        data_list = []

        for x in range(0, len(data)):
            invoicePrice = data[x]['purchaseHistory']['invoicePrice']
            paymentMethod = data[x]['purchaseHistory']['paymentMethodTitle']
            userCountry = data[x]['purchaseHistory']['userCountry']
            documentType = data[x]['purchaseHistory']['doc']['documentType']
            itemTitle = data[x]['purchaseHistory']['doc']['title']
            purchaseTime = data[x]['purchaseHistory']['purchaseTime']
            
            x += 1
           
            data_list.append((purchaseTime, itemTitle, documentType, invoicePrice, paymentMethod, userCountry))

        num_entries = len(data_list)
        if num_entries > 0:
            report = ArtifactHtmlReport('Google Play Store Purchase History')
            report.start_artifact_report(report_folder, 'Google Play Store Purchase History')
            report.add_script()
            data_headers = ('Purchase Timestamp','Item Title','Document Type','Price','Payment Method','User Country') 

            report.write_artifact_data_table(data_headers, data_list, file_found)
            report.end_artifact_report()
            
            tsvname = f'Google Play Store Purchase History'
            tsv(report_folder, data_headers, data_list, tsvname)
            
            tlactivity = f'Google Play Store Purchase History'
            timeline(report_folder, tlactivity, data_list, data_headers)
        else:
            logfunc('No Google Play Store Purchase History data available')