package com.mystream.dom;

import lombok.Getter;
import lombok.Setter;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "Annotator")
public class Annotator {

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
	private String nick;

}
