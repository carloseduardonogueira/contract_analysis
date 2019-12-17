import pandas as pd

def analysis(df_cfts, df_b370, df_ledger):

    worknumbers = pd.DataFrame(columns = [
        "WORKNUMBER", 
        "TO BE INVOICED", 
        "INVOICED B370", 
        "BALANCE B370", 
        "INVOICED LEDGER", 
        "BALANCE LEDGER", 
        "OVERALL BALANCE", 
        "EXPIRED"])
  
    for i in df_cfts.itertuples():
      
        b370_info = df_b370[df_b370["PROJECT_NBR"] == i.WORKNUMBER]
        ledger_info = df_ledger[df_ledger["PROJECT_NBR"] == i.WORKNUMBER]

        currency, column  = ("PESOS","AMTLOC_REP") if i.CURRENCYID == "COP" else ("DOLARES","AMTDLR_REP") 
       
        total_invoiced_ledger = ledger_info.groupby("PROJECT_NBR").sum()[column].values[0] if not ledger_info.empty else "NaN"
        total_invoiced_b370 = b370_info.groupby("PROJECT_NBR").sum()[currency].values[0] if not b370_info.empty else "NaN"
        to_be_invoiced = i.LABORAMOUNT + i.SCHEDCHARGES

        balance_b370 = to_be_invoiced - total_invoiced_b370 if total_invoiced_b370 != "NaN" else to_be_invoiced
        balance_ledger = to_be_invoiced + total_invoiced_ledger if total_invoiced_ledger != "NaN" else to_be_invoiced
        overall_balance = balance_b370 + balance_ledger

        expired = "N" if pd.to_datetime(i.ENDDATE) <= pd.to_datetime("today") else "Y"
       
        if total_invoiced_b370 == "NaN" or total_invoiced_ledger == "NaN":
            worknumbers = worknumbers.append({
                "WORKNUMBER": i.WORKNUMBER, 
                "TO BE INVOICED": float("{0:.2f}".format(to_be_invoiced)), 
                "INVOICED B370":total_invoiced_b370, 
                "BALANCE B370":float("{0:.2f}".format(balance_b370)), 
                "INVOICED LEDGER":total_invoiced_ledger, 
                "BALANCE LEDGER":float("{0:.2f}".format(balance_ledger)), 
                "OVERALL BALANCE":float("{0:.2f}".format(overall_balance)), 
                "EXPIRED":expired}, 
                ignore_index = True)
        else:
            worknumbers = worknumbers.append({
                "WORKNUMBER": i.WORKNUMBER, 
                "TO BE INVOICED": float("{0:.2f}".format(to_be_invoiced)), 
                "INVOICED B370":float("{0:.2f}".format(total_invoiced_b370)), 
                "BALANCE B370":float("{0:.2f}".format(balance_b370)), 
                "INVOICED LEDGER":float("{0:.2f}".format(total_invoiced_ledger)), 
                "BALANCE LEDGER":float("{0:.2f}".format(balance_ledger)), 
                "OVERALL BALANCE":float("{0:.2f}".format(overall_balance)), 
                "EXPIRED":expired}, 
                ignore_index = True)
    
    return worknumbers.to_json(orient = 'index')
    