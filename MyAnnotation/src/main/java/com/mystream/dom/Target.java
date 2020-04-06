package com.mystream.dom;

import com.mongodb.lang.NonNull;
import lombok.Getter;
import lombok.Setter;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

import java.net.URI;

@Document(collection = "Target")
public class Target {

	@Getter
	@Setter
	@NonNull
	private String id;

	@Getter
	@Setter
	private TypeEnum type;

	@Getter
	@Setter
	private String source;

	@Getter
	@Setter
	private Selector selector;

}
