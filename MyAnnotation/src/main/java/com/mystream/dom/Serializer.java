package com.mystream.dom;

import lombok.Getter;
import lombok.Setter;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import java.net.URI;

@Document(collection = "Serializer")
public class Serializer {

	@Id
	@Getter
	@Setter
	private String id;

	@Getter
	@Setter
	private TypeEnum type;

	@Getter
	@Setter
	private String name;

	@Getter
	@Setter
	private String homepage;

}
