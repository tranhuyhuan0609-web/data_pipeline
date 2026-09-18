from database.config_reponsitory import create_config
document = {
    "site_id": "VNExpress",
    "name": "VNExpress",
    "enable": True,
    "base_url": "https://www.vnexpress.net",
    "start_url" : [
        
    ],
    "allowed_domains": [
        "vnexpress.net"
    ],
    "crawl":{
        "delay": 1,
        "max_pages": 100,
        "current_request": 10,
        "timeout": 30
    },
    "selector": {
        "list": {},
        "detail": {}
    }

}
result = create_config(document)