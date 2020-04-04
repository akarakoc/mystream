package com.mystream.dom;

import lombok.Getter;
import lombok.Setter;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import java.net.URI;

@Document(collection = "Serializer")
public class Body {

	@Id
	@Getter
	@Setter
	private Long id;

	@Getter
	@Setter
	private Class type;

	@Getter
	@Setter
	private URI related;

	@Getter
	@Setter
	private String vaule;

	@Getter
	@Setter
	private FormatEnum format;

	@Getter
	@Setter
	private LanguageEnum language;
}
