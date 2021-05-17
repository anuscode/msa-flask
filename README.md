실행방법
```
docker-compose build
docker-compose up -d
```


상품 목록
```
curl -H "Content-Type: application/json" \
-H "USER-TOKEN: 32032dc6-a528-4f2d-b450-0908e07eac5f" \
-X GET http://localhost:5001/
```

단일 상품 상세보기 API
```
curl -H "Content-Type: application/json" \
-H "USER-TOKEN: 32032dc6-a528-4f2d-b450-0908e07eac5f" \
-X GET http://localhost:5001/11
```

알람 트루
```
curl -d '{"item_id":"3"}' \
-H "Content-Type: application/json" \
-H "USER-TOKEN: 32032dc6-a528-4f2d-b450-0908e07eac5f" \
-X POST http://localhost:6001/
```

알람 펄스
```
curl -d '{"item_id":"1"}' \
-H "Content-Type: application/json" \
-H "USER-TOKEN: 32032dc6-a528-4f2d-b450-0908e07eac5f" \
-X DELETE http://localhost:6001/
```

알림 목록
```
curl -H "Content-Type: application/json" \
-H "USER-TOKEN: 32032dc6-a528-4f2d-b450-0908e07eac5f" \
-X GET http://localhost:6001/
```

사용자목록(내림차순)
```
curl -H "Content-Type: application/json" \
-H "USER-TOKEN: 32032dc6-a528-4f2d-b450-0908e07eac5f" \
-X POST http://localhost:7001/
```

최근 본 상품 목록
```
curl -H "Content-Type: application/json" \
-H "USER-TOKEN: 32032dc6-a528-4f2d-b450-0908e07eac5f" \
-X GET http://localhost:7001/visit
```

