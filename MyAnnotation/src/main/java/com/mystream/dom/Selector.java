package com.mystream.dom;

import lombok.Getter;
import lombok.Setter;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import java.net.URI;

@Document(collection = "Selector")
public class Selector {

	@Id
	@Getter
	@Setter
	private String id;

	@Getter
	@Setter
	private Class type;

	@Getter
	@Setter
	private Long start;

	@Getter
	@Setter
	private Long end;

}
