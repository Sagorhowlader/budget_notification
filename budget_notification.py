from typing import List, Tuple

from db_connection import Database
from utils import get_current_month_date


def get_current_month_budgets_for_shop(date: str) -> List[Tuple[int, str, int, int, int]]:
    """Gets the current month budget data for all online shops from the database.

    Parameters:
        date (str): The month to get budget data for, in the format "YYYY-MM-DD".

    Returns:
        A list of tuples, where each tuple contains the shop ID, shop name, budget amount, amount spent, and
        notified amount for a shop.
    """
    query = """SELECT t_shops.a_id, t_shops.a_name, t_budgets.a_budget_amount, t_budgets.a_amount_spent,
               t_budgets.a_notified_amount
        FROM t_shops INNER JOIN t_budgets ON t_shops.a_id = t_budgets.a_shop_id
        WHERE t_shops.a_online = 1 AND t_budgets.a_month = %s
    """
    values = (date,)
    response_data = database.fetch_all(query, values)
    return response_data


def update_shop_status(shop_id: int):
    """Updates the online status of a shop in the database.

     Parameters:
         shop_id (int): The ID of the shop to update the status for.
     """
    # Query to set the shop status to offline
    query = "UPDATE t_shops SET a_online = 0 WHERE a_id =%s"
    # Execute the query
    database.execute(query, (shop_id,))


def update_notification_history(shop_id: int, date: str, notified_amount: int):
    """Updates the notification history for the given shop in the database.

    Parameters:
        shop_id (int): The ID of the shop to update the notification history for.
        date (str): The month to update the notification history for, in the format "YYYY-MM".
        notified_amount (int): The new notified amount for the given month.
    """
    query = """
        UPDATE t_budgets
        SET a_notified_amount = %s
        WHERE a_shop_id = %s AND a_month = %s
    """
    values = (notified_amount, shop_id, date)
    database.execute(query, values)


def handle_notification(shop_id: int, shop_name: str, budget_amount: int, amount_spent: int,
                        expenditures_percentage: float):
    """Handles a notification for a shop that has reached a certain percentage of its budget.

    This includes printing a notification message to the console and updating the notification history in the database
    to prevent sending duplicate notifications.

    Parameters:
        shop_id (int): The ID of the shop to send a notification for.
        shop_name (str): The name of the shop to send a notification for.
        budget_amount (int): The budget amount for the shop.
        amount_spent (int): The current amount spent by the shop.
        expenditures_percentage (float): The percentage of the budget that has been spent.
    """
    print(
        f'Shop ID: {shop_id} Shop Name: ({shop_name}) has reached {expenditures_percentage:.2f}% of the budget for '
        f'month {current_month}. '
        f'Budget: {budget_amount}, '
        f'Expenditure: {amount_spent}  '
        f'Expenditures percentage: ({expenditures_percentage:.2f}%)')
    update_notification_history(shop_id, current_month, budget_amount)


def send_notification(budget_data: List[Tuple[int, str, int, int, int]]):
    """Sends notifications to shops based on their current budget data.

    If the expenditures percentage is 50% or greater, it sends a notification to the shop and updates the
    t_budgets table with the notified amount (used for checking if a notification has already been sent).
    If the percentage is 100% or greater, it sets the shop's online status to 0 in addition to sending the
    notification.

    Parameters:
        budget_data (List[Tuple[int, str, int, int, int]]): A list of tuples, where each tuple contains the shop
            ID, shop name, budget amount, amount spent, and notified amount for a shop.
    """
    for shop_id, shop_name, budget_amount, amount_spent, notified_amount in budget_data:
        expenditures_percentage = amount_spent / budget_amount * 100
        notified_percentage = notified_amount / budget_amount * 100 if notified_amount != '0.0' or None else 0
        if 50 <= expenditures_percentage < 100:
            if notified_percentage > 50:
                print(f"Shop ID: {shop_id}  Shop Name: ({shop_name}) has already send notification.")
                continue
            handle_notification(shop_id, shop_name, budget_amount, amount_spent, expenditures_percentage)
        elif expenditures_percentage >= 100:
            handle_notification(shop_id, shop_name, budget_amount, amount_spent, expenditures_percentage)
            update_shop_status(shop_id)



if __name__ == "__main__":
    # Database Credential
    database_credential = {
        "host": "localhost",
        "user": "root",
        "password": "123",
        "database": "budget_notifications"
    }
    # Initialize the database connection  object
    database = Database(**database_credential)

    # Get the current month data
    current_month = get_current_month_date()

    # Get the current month shop budgets data
    current_month_shop_budgets_data = get_current_month_budgets_for_shop(current_month)
    if current_month_shop_budgets_data:
        # Send notification to shop
        send_notification(current_month_shop_budgets_data)

    # Close the database connection
    database.close()
