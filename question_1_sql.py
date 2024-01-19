Q_1_SQL = """
            WITH accounts_with_opening_dates AS (
            
            SELECT

                a.customer_no,
                a.account_no,
                a.product_type_code,
                a.account_status,
                c.bill_acct,
                
                CASE 
                    WHEN c.open_date
                    THEN strptime(c.open_date, '%Y%m%d')
                    ELSE a.open_date
                END AS account_open_date,
                
            FROM account a
            
            LEFT JOIN credit_card_account c 
            ON a.account_no ILIKE  '%' || c.card_no
            
            )
            
            SELECT
            
                account_no,
                account_open_date
             
            FROM accounts_with_opening_dates 
            
            WHERE (product_type_code = 'BUSS' AND bill_acct = 'Y')
            OR product_type_code IN ('CCRD', 'TRAN', 'SAVG', 'HMLN')
            AND account_status != 'C'
"""