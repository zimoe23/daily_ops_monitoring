import gspread
from config.settings import JSON_CREDS_PATH, GOOGLE_SHEET_ID, TARGET_TAB_NAME
from utils.constants import GSHEET_HEADER
from models.node import Node
import gspread
from datetime import datetime

class GoogleSheetManager:

    def __init__(self):
        gc = gspread.service_account(filename=JSON_CREDS_PATH)
        sh = gc.open_by_key(GOOGLE_SHEET_ID)
        self.worksheet = sh.worksheet(TARGET_TAB_NAME)

    def get_nodes(self) -> list[Node]:
        rows = self.worksheet.get_all_records()
        nodes = []
        

        for row in rows:
            node_type = str(row.get(GSHEET_HEADER.NODE_TYPE.value, ""))
            node = Node(
                node_id=row[GSHEET_HEADER.NODE_ID.value],
                project_id=row[GSHEET_HEADER.PROJECT_ID.value],
                node_name=row.get(GSHEET_HEADER.TASK_NAME.value, ""),
                is_hourly="HOURLY" in node_type.upper(),
                sla_limit=row.get(GSHEET_HEADER.SLA.value, 0),
                current_status=row.get(GSHEET_HEADER.STATUS.value, "")
            )
            nodes.append(node)
        return nodes
    
    def batch_update_status_by_id(self, node_status_list):
        print("batch_update_status_by_id")
        all_rows = self.worksheet.get_all_values()
        headers = [h.strip().lower() for h in all_rows[0]]

        node_col = headers.index(GSHEET_HEADER.NODE_ID.value) + 1
        status_col = headers.index(GSHEET_HEADER.STATUS.value) + 1
        update_col = headers.index(GSHEET_HEADER.LAST_UPDATE.value) + 1

        # Map node_id -> row number, skip empty IDs
        node_row_map = {
            row[node_col - 1].strip(): i
            for i, row in enumerate(all_rows[1:], start=2)
            if row[node_col - 1].strip()
        }

        updates = []
        update_count = 0

        for item in node_status_list:
            nid = str(item.get("node_id", "")).strip()
            if not nid:
                continue

            status = item.get("status", "").strip()
            last_update = item.get("last_update", "").strip()

            if nid in node_row_map:
                row_num = node_row_map[nid]

                updates.append({
                    "range": gspread.utils.rowcol_to_a1(row_num, status_col),
                    "values": [[status]]
                })

                if last_update:
                    updates.append({
                        "range": gspread.utils.rowcol_to_a1(row_num, update_col),
                        "values": [[last_update]]
                    })

                update_count += 1

        if updates:
            self.worksheet.batch_update(updates)
            print(f"Updated {update_count} rows (status + last_update) by node_id.")
                
    def batch_update_status_by_task_name(self, task_status_list):
        print("batch_update_status_by_task_name")
        all_rows = self.worksheet.get_all_values()
        if not all_rows:
            print("Worksheet is empty.")
            return

        headers = [h.strip() for h in all_rows[0]]
        task_col = headers.index(GSHEET_HEADER.TASK_NAME.value) + 1
        status_col = headers.index(GSHEET_HEADER.STATUS.value) + 1
        update_col = headers.index(GSHEET_HEADER.LAST_UPDATE.value) + 1

        # Map task_name -> row number, skip empty names
        task_row_map = {
            row[task_col - 1].strip(): i
            for i, row in enumerate(all_rows[1:], start=2)
            if row[task_col - 1].strip()
        }

        updates = []
        update_count = 0

        for item in task_status_list:
            task_name = str(item.get("task_name", "")).strip()
            if not task_name:
                continue

            status = item.get("status", "").strip()
            last_update = item.get("last_update", "").strip()

            if task_name in task_row_map:
                row_num = task_row_map[task_name]

                updates.append({
                    "range": gspread.utils.rowcol_to_a1(row_num, status_col),
                    "values": [[status]]
                })

                if last_update:
                    updates.append({
                        "range": gspread.utils.rowcol_to_a1(row_num, update_col),
                        "values": [[last_update]]
                    })

                update_count += 1

        if updates:
            self.worksheet.batch_update(updates)
            print(f"Updated {update_count} rows (status + last_update) by task_name.")
        else:
            print("No matching task_name found to update.")
            """
            Updates the sheet based on task_name.
            task_status_list example:
            [
                {"task_name": "odps2oss_vdm_rpt_loan_finder_ext_affluent_w", "status": "Running", "last_update": "2026-03-08 10:12"},
                {"task_name": "exc_pty_mbr_lnd_account_custom_duplicate_d", "status": "Success", "last_update": "2026-03-08 11:05"}
            ]
            """

            all_rows = self.worksheet.get_all_values()
            if not all_rows:
                print("Worksheet is empty.")
                return

            headers = [h.strip() for h in all_rows[0]]

            # Find required columns
            task_col = headers.index(GSHEET_HEADER.TASK_NAME.value) + 1
            status_col = headers.index(GSHEET_HEADER.STATUS.value) + 1
            update_col = headers.index(GSHEET_HEADER.LAST_UPDATE.value) + 1

            # Map task_name -> row number (skip empty task names)
            task_row_map = {
                row[task_col - 1].strip(): i
                for i, row in enumerate(all_rows[1:], start=2)
                if row[task_col - 1].strip()
            }

            updates = []
            update_count = 0

            for item in task_status_list:
                task_name = str(item.get("task_name", "")).strip()
                if not task_name:
                    continue  # skip empty task_name

                status = item.get("status", "").strip()
                last_update = item.get("last_update", "").strip()

                if task_name in task_row_map:
                    row_num = task_row_map[task_name]

                    # Update status
                    updates.append({
                        "range": gspread.utils.rowcol_to_a1(row_num, status_col),
                        "values": [[status]]
                    })

                    # Update last_update if provided
                    if last_update:
                        updates.append({
                            "range": gspread.utils.rowcol_to_a1(row_num, update_col),
                            "values": [[last_update]]
                        })

                    update_count += 1

            if updates:
                self.worksheet.batch_update(updates)
                print(f"Updated {update_count} rows (status + last_update) based on task_name.")
            else:
                print("No matching task_name found to update.")