package com.mystream;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.mongodb.repository.config.EnableMongoRepositories;

@SpringBootApplication
@EnableMongoRepositories({"com.mystream.repo"})
public class MyAnnoationApplication {

	public static void main(String[] args) {
		SpringApplication.run(MyAnnoationApplication.class, args);
	}

}
