## 应用简介
本应用展示了使用函数工作流（FnF）和函数计算（FC）实现订单多步骤流程处理，详见[文档](https://help.aliyun.com/document_detail/122482.html)。通过 FnF 以下功能确保了在依赖不可用或是系统宕机等复杂的生产环境中也能最大限度地实现订单流程事务（transaction）语义，降低人工干预的频率：
1. 对单步骤支付失败等错误进行自定义重试 (retry)。
2. 重试耗尽后通过错误捕获（catch）执行补偿逻辑，例如取消预订或报警请求人工介入。
3. 对每个步骤状态的持久化，在宕机断网等环境下也能保证流程状态不丢失，环境恢复后流程执行随之恢复。

## 部署
本示例所需要的 FnF 的流程和 FC 函数已经在 teamplate.yml 模板中定义，只需要通过 fun 工具即可一键部署

```bash
# git clone 该项目后在根目录 trip-booking-order-processing 下执行：
fun deploy
```

## 执行
在[函数工作流控制台](https://fnf.console.aliyun.com/fnf/cn-hangzhou/flows) 相应流程下使用下面的 JSON object 作为输入，其中以 *_result 的值来模拟预定操作成功或失败，例如 `"book_hotel_result": "failed"` 时，`BookHotel` 步骤会失败，以此演示错误捕获，重试和补偿逻辑的执行。

```json
{
   "trip_order_id": "happy-trip-id-1",
   "book_train_ticket_result": "succeeded",
   "book_flight_ticket_result": "succeeded",
   "book_hotel_result": "failed",
   "cancel_flight_ticket_result": "succeeded",
   "cancel_train_ticket_result": "succeeded"
}
```

![trip-order-processing](images/trip_order_processing.png)


