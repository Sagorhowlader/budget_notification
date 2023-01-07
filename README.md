# Budget Notification

The script first gets the current month budget data for all online shops from the database. It then iterates through
each shop's data and calculates the expenditure's percentage. If the percentage is 50% or greater, it sends a
notification to the shop and updates the notification history in the database. If the percentage is 100% or greater, it
sets the shop's online status to offline in the database.

### Requirements

- Python 3.8.0+
- MySQL Connector 2.2.9+
- MySQL 8.0
- Database Migration

### Database Migration

**import the `db.sql` first than import new adopt new schema `migration.sql` in your database**
or

    ALTER TABLE t_budgets ADD new_field DECIMAL(10,2) DEFAULT 0;

### Installation

A step by step guide on how to get the development environment running.

**1. Clone the repository**

     git clone https://github.com/Sagorhowlader/budget_notification

**2. Navigate to the project directory**

    cd budget_notification

**3. Install the dependencies**

    pip install -r requirements.txt

**4. Before running the code, you need to change the `database_credentials` in the `budget_notification.py` file:

```json
    {
  "host": "DATABASE HOSTNAME",
  "user": "DATABASE USER",
  "password": "DATABASE USER PASSWORD",
  "database": "DATABASE NAME"
}
```

**5. Running the project**

    python budget_notification.py 

### Functions

`get_current_month_budgets_for_shop(date: str) -> List[Tuple[int, str, int, int, int]]`:
This function retrieves the current month's budget data for all online shops from the database. It takes a single
parameter, date, which is a string in the format "YYYY-MM" representing the month to retrieve budget data for. It
returns a list of tuples, where each tuple contains the shop ID, shop name, budget amount, amount spent, and notified
amount for a shop.

`update_shop_status(shop_id: int)`:
This function updates the online status of a shop in the database. It takes a single parameter, shop_id, which is the ID
of the shop to update the status for.

`update_notification_history(shop_id: int, date: str, notified_amount: int)`:
This function updates the notification history for the given shop in the database. It takes three parameters: shop_id,
which is the ID of the shop to update the notification history for; date, which is the month to update the notification
history for, in the format "YYYY-MM-DD"; and notified_amount, which is the new notified amount for the given month.

`handle_notification(shop_id: int, shop_name: str, budget_amount: int, amount_spent: int, expenditures_percentage: float)`:
his function handles a notification for a shop that has reached a certain percentage of its budget. It takes five
parameters: shop_id, which is the ID of the shop to send a notification for; shop_name, which is the name of the shop;
budget_amount, which is the budget amount for the shop; amount_spent, which is the current amount spent by the shop; and
expenditures_percentage, which is the percentage of the budget that has been spent. It prints a notification message to
the console and updates the notification history in the database

`send_notification(budget_data: List[Tuple[int, str, int, int, int]])`:
Sends notifications to shops based on their current budget data.

### Acknowledgement

**1.Does your solution avoid sending duplicate notifications?**

```To avoid sending duplicate notifications, Retrieve current budget data for all online shops from the t_budgets table in the database.For each shop, check the notified amount in the budget data. If the notified amount is 0, send a notification to the shop and update the notified amount in the t_budgets table with the budget amount. If the notified amount is equal to or greater than 50% of the budget amount, print a message indicating that a notification has already been sent for that month. If the expenditures percentage is equal to or greater than 100%, update the notified amount in the t_budgets table with the budget amount.```

**2. How does your solution handle a budget change after a notification has already been sent?**

```If the budget changes after a notification has already been sent, my solution is first check the notified amount for the shop in the t_budgets table. If the notified amount is less than 50% of the new budget amount, the function would update the notified amount in the t_budgets table with the new budget amount. If the notified amount is equal to or greater than 50% of the new budget amount, the function would print a message indicating that a notification has already been sent for that month. If the notified amount is equal to or greater than 100% of the new budget amount, the function would not send a notification or update the notified amount. This ensures that notifications are only sent once for each shop and month, even if the budget changes.```

###Limitation
- The script only working `current_month_date` so we need current date data to send notification.