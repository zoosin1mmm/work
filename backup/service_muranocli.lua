--#ENDPOINT POST /muranocli/relationalDB/insert
Postgresql.query({ sql = request.body.createSQL })
return Postgresql.query({ sql = request.body.insertSQL })

--#ENDPOINT POST /muranocli/timer
return Timer.sendAfter(request.body)