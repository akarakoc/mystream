package com.mystream.dom;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.mongodb.lang.NonNull;
import lombok.Getter;
import lombok.Setter;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

import java.net.URI;

@Document(collection = "Body")
public class Body {

	@Getter
	@Setter
	@NonNull
	@Field("id")
	@JsonProperty("@id")
	private String id;

	@Getter
	@Setter
	@NonNull
	private TypeEnum type;

	@Getter
	@Setter
	@NonNull
	private FormatEnum format;

	@Getter
	@Setter
	private String related;

	@Getter
	@Setter
	private String value;

	@Getter
	@Setter
	private LanguageEnum language;
}
