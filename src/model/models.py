from sqlmodel import String, Float, Integer, BigInteger, Text, Boolean, Field
from datetime import datetime
from src.core.database import BaseTable

class Transaction(BaseTable, table=True):
    __tablename__ = "transaction"

    # 基本信息
    tenant_id: str = Field(
        sa_type=String(32),
        nullable=True,
        default="default_tenant",
        sa_column_kwargs={"comment": "租户ID"}
    )
    client_id: int = Field(
        sa_type=BigInteger,
        nullable=False,
        sa_column_kwargs={"comment": "顾客ID"},
        foreign_key="client.id"
    )
    sku_id: int = Field(
        sa_type=BigInteger,
        nullable=False,
        sa_column_kwargs={"comment": "SKU ID"},
        foreign_key="sku.id"
    )
    quantity: int = Field(
        sa_type=Integer,
        nullable=False,
        default=1,
        sa_column_kwargs={"comment": "购买数量"}
    )
    amount: float = Field(
        sa_type=Float,
        nullable=False,
        sa_column_kwargs={"comment": "总价格(實際成交)"}
    )
    currency: str = Field(
        sa_type=String(16),
        nullable=False,
        sa_column_kwargs={"comment": "货币类型"}
    )
    transaction_date: datetime = Field(
        nullable=False,
        sa_column_kwargs={"comment": "交易时间"}
    )

    # 支付和物流
    payment_method: str = Field(
        sa_type=String(32),
        nullable=True,
        sa_column_kwargs={"comment": "支付方式"}
    )
    shipping_status: str = Field(
        sa_type=String(32),
        nullable=True,
        sa_column_kwargs={"comment": "物流状态"}
    )

    # 促销和折扣
    discount: float = Field(
        sa_type=Float,
        default=0.0,
        sa_column_kwargs={"comment": "折扣金额"}
    )
    promotion_id: str | None = Field(
        sa_type=String(64),
        nullable=True,
        sa_column_kwargs={"comment": "促销活动ID"}
    )

    # 备注字段
    comment: str | None = Field(
        sa_type=String(500),
        nullable=True,
        sa_column_kwargs={"comment": "交易备注"}
    )

class Conversation(BaseTable, table=True):
    __tablename__ = "conversation"

    tenant_id: str = Field(sa_type=String(32), sa_column_kwargs={"comment": "租户ID"})
    bot_id: int = Field(sa_type=BigInteger, sa_column_kwargs={"comment": "智能体ID"})
    llm_api_type: str = Field(
        sa_type=String(32), sa_column_kwargs={"comment": "大模型平台类型"}
    )
    llm_conversation_id: str = Field(
        sa_type=String(64), sa_column_kwargs={"comment": "大模型平台会话ID"}
    )
    title: str = Field(sa_type=String(32), sa_column_kwargs={"comment": "对话标题"})
    chat_mode: str = Field(sa_type=String(32), sa_column_kwargs={"comment": "对话模式"})
    chat_user_source: str = Field(
        sa_type=String(32), sa_column_kwargs={"comment": "对话用户来源"}
    )
    chat_user_id: str = Field(
        sa_type=String(64), sa_column_kwargs={"comment": "对话用户ID"}
    )

class Message(BaseTable, table=True):
    __tablename__ = "message"

    tenant_id: str = Field(sa_type=String(32), sa_column_kwargs={"comment": "租户ID"})
    chat_id: int = Field(sa_type=BigInteger, sa_column_kwargs={"comment": "对话ID"})
    llm_api_type: str = Field(
        sa_type=String(32), sa_column_kwargs={"comment": "大模型平台类型"}
    )
    role: str = Field(sa_type=String(16), sa_column_kwargs={"comment": "角色"})
    message_type: str = Field(
        sa_type=String(16), sa_column_kwargs={"comment": "消息类型"}
    )
    message_data: str = Field(sa_type=Text, sa_column_kwargs={"comment": "消息数据"})
    total_token: int = Field(
        sa_type=Integer, default=0, sa_column_kwargs={"comment": "总token数"}
    )
    input_token: int = Field(
        sa_type=Integer, default=0, sa_column_kwargs={"comment": "输入token数"}
    )
    output_token: int = Field(
        sa_type=Integer, default=0, sa_column_kwargs={"comment": "输出token数"}
    )

class Client(BaseTable, table=True):
    __tablename__ = "client"

    # Primary identifiers （访客留联系方式时设置）
    tenant_id: str = Field(
        sa_type=String(32),
        nullable=False,
        description="外部系统映射字段: enterprise_id",
        sa_column_kwargs={"comment": "租户ID"},
        index=True,
    )
    openid: str | None = Field(
        sa_type=String(64),
        default="",
        description="外部系统映射字段: __openid",
        sa_column_kwargs={"comment": "微信用户标识"},
        index=True,
    )
    follow_source: str | None = Field(
        sa_type=String(32),
        default="",
        description="外部系统映射字段: __follow_source",
        sa_column_kwargs={"comment": "微信关注来源"},
    )

    # Basic information
    name: str | None = Field(
        sa_type=String(50), default="", sa_column_kwargs={"comment": "顾客姓名"}
    )
    age: int | None = Field(
        sa_type=Integer,
        default=0,
        sa_column_kwargs={"comment": "顾客年龄"},
        ge=0,
        le=150,
    )
    gender: str | None = Field(
        sa_type=String(8), default="", sa_column_kwargs={"comment": "顾客性别"}
    )

    # Contact information
    email: str | None = Field(
        sa_type=String(128),
        default="",
        sa_column_kwargs={
            "comment": "电子邮箱地址",
        },
    )
    tel: str | None = Field(
        sa_type=String(16),
        default="",
        sa_column_kwargs={
            "comment": "联系电话",
        },
    )
    address: str | None = Field(
        sa_type=String(256), default="", sa_column_kwargs={"comment": "联系地址"}
    )
    contact: str | None = Field(
        sa_type=String(50), default="", sa_column_kwargs={"comment": "联系人姓名"}
    )

    # Social media handles
    qq: str | None = Field(
        sa_type=String(64),
        default="",
        sa_column_kwargs={
            "comment": "QQ账号",
        },
    )
    weibo: str | None = Field(
        sa_type=String(64), default="", sa_column_kwargs={"comment": "微博账号"}
    )
    weixin: str | None = Field(
        sa_type=String(64), default="", sa_column_kwargs={"comment": "微信账号"}
    )

    # Additional information
    comment: str | None = Field(
        sa_type=String(500),
        default="",
        description="来源: 系统操作",
        sa_column_kwargs={"comment": "备注说明"},
    )

class Spu(BaseTable, table=True):
    __tablename__ = "spu"

    tenant_id: str = Field(max_length=256, description="该商品所属的商户id，支持多租户")
    product_knowledge_id: int = Field(default=0, description="该商品SPU所属知识库ID")
    external_id: str | None = Field(default="", max_length=256, description="外部系统id")

    # SKU相关字段
    main_sku: str | None = Field(default="", max_length=1024, description="主sku code")
    # options: dict = Field(sa_column=JSON, description="决定sku的可选商品选项")

    # 商品定位字段
    title: str = Field(max_length=765, description="该商品在电商平台展示的标题")
    # specifications: dict = Field(sa_column=JSON, description="在商品页面上的结构化描述")
    description: str | None = Field(
        default="", max_length=24573, description="商品在电商平台上的文字描述、子标题"
    )
    platform: str | None = Field(max_length=32, description="商品上架的电商平台（统一大写，例如：SHOPEE, LAZADA）")
    # breadcrumb: dict = Field(sa_column=JSON, description="五级分类路径")
    brand: str | None = Field(default="", max_length=128, description="该商品所属品牌")

    # 链接字段
    platform_url: str | None = Field(max_length=2048, description="主动推送商品展示页")

    # 量价字段
    initial_price: float | None = Field(description="商品初始单价")
    currency: str | None = Field(max_length=16, description="该商品计价所用的货币，应设置为ISO 4217标准枚举值")
    # payments: dict = Field(sa_column=JSON, description="包含计价单位、最低购买数量、信用卡分期付款期数")

    # 物流字段
    # logistics: dict = Field(sa_column=JSON, description="物流细节")

    # 口碑字段
    query_counts: int = Field(default=0, description="被访客直接询问的次数")
    recall_counts: int = Field(default=0, description="AI客服推荐给访客的次数")
    avg_sales_volume: int = Field(default=0, description="该商品历史累计销量")
    mon_sales_volume: int = Field(default=0, description="该商品当月累计销量")
    rating: float = Field(default=-1.0, description="该商品的售后买家评分")

    # 动态字段
    # promotions: dict = Field(sa_column=JSON, description="活动时段以及对应的折扣方式等")
    status: str | None = Field(default="", max_length=50, description="在售、促销、缺货、下架、预售、新品等")

class Sku(BaseTable, table=True):
    __tablename__ = "sku"

    tenant_id: str = Field(max_length=256, description="所属商户ID，支持多租户")
    spu_id: int = Field(description="该sku 的上级 spu_id")
    sku_code: str = Field(max_length=1024, description="商户自定义SKU编码，对应旺销王sku_code")
    external_id: str | None = Field(default="", max_length=256, description="外部系统id， 对应旺销王 platform_sku_id")

    # 商品定位字段
    title: str = Field(max_length=765, description="该商品在电商平台展示的标题")

    # 链接字段
    image_url: str = Field(default="", max_length=2048, description="SKU图片URL，对应旺销王sku_pic，一个SKU一张图")

    # 量价字段
    initial_price: float = Field(description="商品初始单价，对应旺销王price")
    currency: str = Field(max_length=16, description="该商品计价所用的货币，对应旺销王currency，应设置为ISO 4217标准")

    # 物流字段
    stock_value: int = Field(default=0, description="该商品的库存数量，对应淘宝千牛后台和旺销王stock_value")

class Agent(BaseTable, table=True):
    __tablename__ = "agent"
    
    query: str = Field(index=True)
    analysis: str | None = Field(default=None)
    data: str | None = Field(default=None)
