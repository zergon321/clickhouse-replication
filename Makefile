rm-volumes:
	docker volume ls --filter name=replication.* -q | xargs docker volume rm
