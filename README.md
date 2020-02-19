## 应用简介
订单处理业务通常对事务性要求较高（全部预订支付成功或者全部退订成功）。现代订单系统往往需要分步骤调用多个分布式服务（如火车票，机票，酒店平台）的接口完成预订或退订操作，每个服务的可用性不尽相同。比较常见的提高分布式事务能力的方案是借助工作流引擎实现 Saga 模式，支持订单级别的事务。本应用展示了使用函数工作流（FnF）和函数计算（FC) 确保即使在严苛负责的生产环境中也能最大限度地实现订单流程事务（transaction）语义，降低人工干预的频率，减少用户反馈和投诉，提升用户体验。

## 本地开发
本示例所需要的 FnF 的流程和 FC 函数已经在 teamplate.yml 模板中定义，只需要通过 fun 工具即可一键部署

```bash
# git clone 该项目后在根目录 trip-booking-order-processing 下执行：
fun deploy
```

* FnF 流程目录：flows/
* FC 函数目录：functions/

## 调用示例
点击`部署应用`创建资源完成，点击 Function Flow 资源跳转到 trip-order-processing 流程，使用以下 JSON 对象点击`开始流程` ：

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

## 工作原理
如下图所示，FnF 流程定义了订单处理的流程逻辑。流程的每个步骤由 FC 函数实现调用不同平台微服务接口。该订单第一步预订火车票，第二步预订机票，最后一步预订酒店。三个步骤分别调用了不同平台的微服务接口，每个步骤都存在失败的概率。假设最后一步预订酒店失败，按照定义的逻辑，流程将会跳转到`取消机票预订`并在下一步骤执行`取消火车票预订`。假如取消步骤也遇到了错误，此时订单无法自动补偿，需要通知客服介入手动处理订单，保证用户体验。函数工作流提供了下列功能支撑了订单可以按照既定逻辑可靠执行：

1. **重试（retry)：** 对单步骤支付失败等错误进行自定义重试。
2. **捕获 (catch)：** 重试耗尽后通过捕获错误，通过 `goto` 跳转到补偿逻辑步骤，例如取消预订或报警请求人工介入。
3. **状态持久化：** 对每个步骤产生的事件的持久化，即使在服务宕机断网升级等非预期情况中也能保证流程状态不丢失，环境恢复后流程执行随之恢复。

![fnf-fc-CN](https://img.alicdn.com/tfs/TB1bOMSvHj1gK0jSZFOXXc7GpXa-1541-1141.png)

