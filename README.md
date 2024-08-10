Explanation of the Application:

SNS Topic: Represents the event of an order being placed. When an order is placed, a message is published to this topic.

SQS Queue: Receives the message from the SNS topic. The queue ensures that even if the processing is slow or the Lambda function fails, the message remains in the queue for future retries.

SES: Simple Email Service will be used as our Email Server in this scenario

Lambda Function: Processes the order by:

Updating the order status in the DynamoDB table.
Reducing the inventory counts in the DynamoDB inventory table.
Sending a confirmation email to the customer.

DynamoDB Table: DynamoDB table will be used for storing our Orders and Inventory count

Cloudwatch: Cloudwatch will be used for monitoring and troubleshooting incase there is issue, our Lambda function is configured to send Logs to Lambda

Real-World Use Case
In a real-world e-commerce platform, this architecture ensures reliable and scalable order processing. Even if the inventory service or email service is temporarily unavailable, the system continues to function without losing orders. Each step in the processing pipeline can be independently scaled and managed.


Let's Test our Example then

To test our example, we will publish a message to the SNS topic,this will simulates an order being placed. Here's an example of how we can do this:

We will use the AWS CLI to Publish the Order Message to SNS. See sample command below:

aws sns publish \
    --topic-arn arn:aws:sns:us-west-2:YOUR_ACCOUNT_ID:order-notifications-topic \
    --message '{
        "order_id": "12345",
        "customer_email": "customer@example.com",
        "items": [
            {"item_id": "item001", "quantity": 2},
            {"item_id": "item002", "quantity": 1}
        ]
    }'



NOTE: In our Scenario, we must verify both our Sender Email and Recipient Email,


Sandbox Restrictions:

SES accounts start in a sandbox mode by default. In this mode, we can only send emails to and from verified email addresses. This includes any recipient email addresses.
This restriction is in place to prevent spam and to help you test your email sending capabilities without risk of sending unsolicited emails.


Email Verification:

SES requires you to verify each email address (both sender and recipient) to ensure that the emails are being sent to willing recipients, even during testing.
Verification involves Amazon SES sending a confirmation email to the specified address, and the recipient must click the link in the email to verify it.


Moving Out of the Sandbox:

Once you’re ready to send emails to unverified recipients, you can request to have your account moved out of the sandbox. When your account is in production mode, you no longer need to verify recipient emails, although sender emails must still be verified.

Implications for our Scenario
as we are using SES in sandbox mode for our e-commerce order processing system:

All customer emails that we want to send order confirmations to must be verified.
To avoid verification for each customer, we would need to apply to move our SES account out of sandbox mode. Once our account is out of the sandbox, we can send emails to any address without verifying it first.


How to Move SES Out of the Sandbox
To lift these restrictions and send emails to unverified recipients:

Request Production Access:

In the AWS SES console, navigate to “Service Quotas” and request production access.
we will need to provide some information about our use case, the volume of emails we intend to send, and how we handle unsubscribe requests, among other things.


Approval:

AWS reviews the request and, if approved, we can send emails to any address without prior verification.

Summary for our USE CASE
When using SES in the sandbox, verifying customer emails ensures that our testing does not unintentionally send emails to unauthorized recipients. Moving out of the sandbox allows us to send emails to any customer without needing to verify each email address first.
