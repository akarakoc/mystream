package com.mystream.dom;

import lombok.Getter;
import lombok.Setter;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "Sequence")
public class Sequence {

	@Id
	@Getter
	@Setter
	String id;

	@Getter
	@Setter
	Long sequence;
}
