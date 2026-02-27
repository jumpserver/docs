# Work Order
!!! tip ""
    - The work order feature is mainly responsible for requesting and reviewing authorization work orders, as well as managing command filtering and asset login reviews. JumpServer authorization requests support a two-level approval workflow. The work order feature supports controlling user login request behaviors and command filtering functions. After users submit a work order request and the corresponding approvers in the configured process approve it, the user can obtain permissions for the requested assets or user login requests and command filtering.
  
## 1 My Requests
- The My Requests page mainly displays detailed records of work orders created by users. On this page, you can request work orders.
  
**Request Work Order**

![image](../../../img/workorder01.png)
![image](../../../img/workorder02.png)

Parameter Description

| Parameter               | Description                                                               |
|--------------------|--------------------------------------------------------------------|
| Title               | The title of the work order.                                                     |
| Organization             | The organization for which the work order is requesting permissions and where the JumpServer user is located.                   |
| Node               | The asset that the JumpServer user is requesting. Node refers to requesting permissions for all assets under an entire node.   |
| Asset               | The asset that the JumpServer user is requesting.                                       |
| Request Account           | The login account for the asset that the JumpServer user is requesting.                       |
| Operation               | The action permissions that the JumpServer user is requesting to have.                               |
| Start Date, Expiration Date | The period during which the user's requested permissions are valid.                                         |

**View Work Order**

- Click the created <Work Order Title> button to enter the work order details page. The work order details page includes the work order's basic information, request information, and approvers. On this page, you can also communicate with approvers.
![image](../../../img/workorder03.png)

**Cancel Work Order**

- You can manually cancel the work order on the work order details page.
![image](../../../img/workorder04.png)

## 2 Awaiting My Approval

- On the Awaiting My Approval page, click the <Work Order Name> button to review and approve the work order. When approvers view the work order, they can modify the permissions for assets, accounts, operations, etc. requested by the applicant.

![image](../../../img/workorder05.png)
![image](../../../img/workorder06.png)

- In addition to approving on the JumpServer page, JumpServer also supports direct work order approval through enterprise WeChat and DingTalk. When the approver's enterprise WeChat or DingTalk is bound, the approver can approve applicant work orders in real-time on enterprise WeChat or DingTalk.

![image](../../../img/workorder07.png)
