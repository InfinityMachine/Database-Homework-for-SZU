# **Introduction / 介绍**

To experience the Windows client of this project, navigate to the `build/windows` folder inside the `main` directory and double-click `main.exe`. This will launch the Windows client of the project.

> 若要体验本项目的 Windows 客户端，请进入 `main` 文件夹中的 `build/windows` 文件夹，然后双击 `main.exe`。即可启动本项目的 Windows 客户端。

* **Note**: The backend database of this project is fully deployed on a cloud server. Therefore, you do not need to set up any databases or data on your local machine to experience the complete functionality of this project.

  > **注意**：本项目的后端数据库完全部署在云服务器上，因此，您无需在本机环境上准备任何数据库或数据，即可体验本项目的完整功能。

* **Tip**: Since the project's database is deployed on Microsoft's Azure cloud server, the application may take a longer time to load in certain situations (up to 10 seconds, especially when users open the orders page). Therefore, if the application does not respond immediately after clicking a button, please wait patiently for a few seconds.

  > **提示**：由于本项目的数据库部署在微软 Azure 云端服务器上，因此，在某些情况下（尤其是当用户打开订单页面时），应用程序将需要较长的时间加载（最多可能 10 秒钟）。因此，当您点击某个按钮时，如果应用程序没有立即响应，请耐心等待几秒钟。

* **Administrator Account Reminder**: Direct registration of administrator accounts is not allowed on the frontend. To experience administrator features, please use the built-in administrator account and password:

  > **提醒**：由于不允许在前端中直接注册管理员账号，因此，若要体验管理员功能，请使用内置的管理员账号和密码：

  * **Username**: admin
  * **Password**: admin

* **Security Caution**: For the completeness of the code functionality, the `DataModel.py` file contains my cloud database password in plain text. To ensure the security of my database, please make sure to remove the corresponding information from the `DataModel.py` file if you intend to publish or distribute this code.

  > **安全性提醒**：为了代码功能的完整性，我在名为 `DataModel.py` 的代码文件中明文引用了我的云端数据库（私人购买）的密码。为了保证我的数据库的安全性，若您要公开或传播此代码，请务必从 `DataModel.py` 文件中抹去相应信息。

# **User Guide / 操作指引**

## **Launching the Application**

![Home Page](https://typora-infinitymachine.oss-cn-shenzhen.aliyuncs.com/typora/image-20241222050358507.png)

* **Home Page**: Upon launching the application, you will see the home page displaying various products available for purchase.

  > **起始页面**：启动应用程序后，您将看到显示各种可购买商品的首页。

## **Main Page**

![Main Page](https://typora-infinitymachine.oss-cn-shenzhen.aliyuncs.com/typora/image-20241222050653818.png)

* **Description**: The main page displays all product data, including product names, descriptions, prices, and images, which are stored in a cloud database or cloud-based image hosting service.

  > **描述**：主页面展示所有商品数据，包括商品名称、描述、价格和图片，这些数据存储在云端数据库或云端图床中。

## **Menu Interaction**

![Menu Interaction](https://typora-infinitymachine.oss-cn-shenzhen.aliyuncs.com/typora/image-20241222051033955.png)

* **Action**: Clicking the menu button at the top left corner.

  > **操作**：点击左上角的菜单按钮。

  * **Result**: A login panel will pop up on the left side of the main interface.

    > **结果**：将在主界面的左侧弹出登录栏。

  * **User Options**: Enter existing credentials or register a new account.

    > **用户选项**：输入已有的账号和密码或注册一个新账号。

  * **Navigation**: Click the back button at the top left of the login panel to return to the previous page.

    > **导航**：点击登录栏左上角的返回按钮，返回到上一级页面。

## **Post-Login Interface**

![Post-Login](https://typora-infinitymachine.oss-cn-shenzhen.aliyuncs.com/typora/image-20241222051409986.png)

* **Description**: After logging in, the login panel updates to reflect the user’s status. The interface adapts based on the user’s permissions.

  > **描述**：用户登录后，登录栏会更新以反映用户的状态。界面根据用户的权限进行适配。

## **Shopping Cart Interaction**

![Shopping Cart](https://typora-infinitymachine.oss-cn-shenzhen.aliyuncs.com/typora/image-20241222051243603.png)

* **Action**: After logging in and selecting products, clicking the shopping cart button at the top right corner.

  > **操作**：用户登录并挑选商品后，点击右上角的购物车按钮。

  * **Options**:

    * **Left Button**: Submit the cart contents to an order, which also clears the user’s cart.

      > **左侧按钮**：将购物车中的内容提交为订单，同时清空用户的购物车。

    * **Right Button**: Navigate to the orders page.

      > **右侧按钮**：进入订单页面。

## **Orders Page**

![Orders Page](https://typora-infinitymachine.oss-cn-shenzhen.aliyuncs.com/typora/image-20241222051033955.png)

* **Description**: Users can view their order information and order details here. They can apply for a refund by clicking the "Request Refund" button. After the refund request is processed by an administrator, users can view the administrator's reason for processing.

  > **描述**：用户可以在此查看他们的订单信息和订单详细信息。通过点击“Request Refund”按钮，用户可以为某个订单申请退款。当用户的退款申请被管理员处理后，用户可以查看管理员处理的理由。

## **Refund Request Interface**

![Refund Request](https://typora-infinitymachine.oss-cn-shenzhen.aliyuncs.com/typora/image-20241222032224639.png)

* **Action**: User initiates a refund request for a specific order.

  > **操作**：用户针对某个订单发起退款申请。

  * **Requirement**: Users need to provide a reason for requesting a refund.

    > **需求**：用户需要填写申请退款的理由。

## **Post-Refund Processing Interface**

![Post-Refund Processing](https://typora-infinitymachine.oss-cn-shenzhen.aliyuncs.com/typora/image-20241222032350357.png)

* **Description**: After an administrator processes a user's refund request, the user can view the administrator's reason for processing.

  > **描述**：当管理员处理用户的退款申请后，用户可以查看管理员处理的理由。

## **Administrator Login Interface**

![Admin Login](https://typora-infinitymachine.oss-cn-shenzhen.aliyuncs.com/typora/image-20241222032724383.png)

* **Action**: When the administrator logs in.

  > **操作**：当管理员登录后。

  * **Result**: The "Admin" option appears at the bottom of the login panel, allowing the administrator to access the management page.

    > **结果**：“Admin”选项出现在登录栏的底部，管理员可以点击该选项进入管理页面。

## **Management Page**

![Management Page](https://typora-infinitymachine.oss-cn-shenzhen.aliyuncs.com/typora/image-20241222032952313.png)

* **Description**: Administrators can view and manage users' refund requests here.

  > **描述**：管理员可以在此查看和管理用户的退款请求。

## **Refund Processing Interface**

![Refund Processing](https://typora-infinitymachine.oss-cn-shenzhen.aliyuncs.com/typora/image-20241222033125354.png)

* **Action**: When an administrator processes a refund request.

  > **操作**：当管理员处理某个退款请求时。

  * **Requirement**: Administrators need to provide a reason for processing.

    > **需求**：管理员需要填写处理原因。

