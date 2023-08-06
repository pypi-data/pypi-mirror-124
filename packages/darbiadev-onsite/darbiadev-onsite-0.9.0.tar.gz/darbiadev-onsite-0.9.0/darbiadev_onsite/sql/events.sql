SELECT Event.ID_Event,
       Event.timestamp_Creation,
       Event.timestamp_Modification,
       Event.sts_Priority,
       Event.id_Order,
       Event.id_OrderDesLoc,
       Event.id_ProductionEvent,
       Event.ct_ProductionEventName,
       Event.id_Machine,
       Event.ct_MachineName,
       Event.date_Scheduled,
       Event.cn_id_Design,
       Event.ct_DesignTitle,
       Event.ct_Location,
       Event.cn_ColorsTotal,
       Event.cn_StitchesTotal,
       Event.Qty
FROM Event
WHERE Event.id_Order = {order_number}
