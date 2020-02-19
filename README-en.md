## Introduction
Transactions are essntial to e-commerce order processing, customers expect either an order is succeessful or failed without making any partial payment. Modern ording processing systems usually involve calling multiple distributed microservices to complete a single order, and each step could fail due to different service availability and state. Implementing Saga pattern based on workflow engines is common to provide better transactional guarantee. This application demostrates using Function Flow (FnF) and Function Compute (FC) to implement reliable transactions even with unavailable dependencies to reduce human interventions and customer complaints.

## Deployment and invocation

Click `Deploy` and ROS will automatically create necessary FnF Flow and FC Functions required for this demo. After the resources are deployment is finished, click the `trip-order-processing` to redirect to Function Flow console and start an execution with the following JSON object as the input.

```json
{
   "trip_order_id": "happy-trip-id-1",
   "book_train_ticket_result": "succeeded",
   "book_flight_result": "succeeded",
   "book_hotel_result": "succeeded",
   "cancel_flight_result": "succeeded",
   "cancel_train_ticket_result": "succeeded"
}
```

## Dive deep
The following figure shows the order processing logic implemented by FnF. A FC function will be invoke in each step of the flow to mock a booking or cancel operation. In this trip order, it first buys a train ticket and then books a flight and finally books a hotel room. The 3 steps involve 3 different microservices and each remote call has a chance to fail. Assume that the final `BookHotel` step failed, the flow will execute the `CancelFlight` step followed by `CancelTrainTicket`. If the cacel operation also encountered failure, then the order is not auto-recoverable and requires customer support to process. Function Flow provides the following functionalities to guarantee the order can be reliably executed as expected.

1. **Retry:** custom retry policy can be specified for each step.
2. **Catch:** after exhausting retries, errors can catched and using the `goto` property to cancel booking or sending alert for human intervention.
3. **State persistence:** FnF persists events produced during flow executions and is able to replay the events to recover flow execution states even with unpredicted service crash and network partitioning.

![fnf-fc-EN](https://img.alicdn.com/tfs/TB1PKZSvUY1gK0jSZFCXXcwqXXa-1541-1141.png)

## Development and Deployment
All the related flow and functions are already defined in the `template.yml`, the project can be deployed with [fun](https://github.com/alibaba/funcraft) tool

```bash
# In the project root directory run fun deploy command
fun deploy
```