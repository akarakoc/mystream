package com.mystream.config;

import com.mongodb.MongoClient;
import com.mongodb.MongoClientURI;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.mongodb.repository.config.EnableMongoRepositories;

import java.net.UnknownHostException;

@Configuration
public class MongoConfig {
	@Value("${spring.data.mongodb.uri}")
	private String uri;


	@Bean(name = "mongoClient")
	public MongoClient mongo() throws UnknownHostException {
		return new MongoClient(new MongoClientURI(uri));
	}
}

