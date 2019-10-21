
.PHONY: test
test:
	bash test.sh

.PHONY: server
server:
	@# nginx requires absolute paths to it's config argument
	@nginx -p "$(shell pwd)" -c "$(shell pwd)/nginx.conf"
