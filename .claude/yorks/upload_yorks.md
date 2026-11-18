上传
   前端 → POST /api/upload
   返回 { key: "upload/abc.jpg", url: "https://...签名..." }
   前端立刻预览 → 直接用 url 塞进 <img src>

② 保存
   前端 → POST /api/lab/update/image  { imageKey: "upload/abc.jpg" }
   数据库只存 key（不能存 url，会过期）

③ 读取/展示
   前端 → GET /api/lab/list
   后端读出 Lab.image = "upload/abc.jpg"
     → get_temporary_url(key) 现签一个新 url
   返回 { image: "...新签名 url..." }
   前端用返回的 url 展示
