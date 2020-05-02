package com.mystream.dom;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.mongodb.lang.NonNull;
import com.mystream.dom.selector.Selector;
import lombok.Getter;
import lombok.Setter;
import org.springframework.data.mongodb.core.mapping.Document;

import java.util.List;

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
	@JsonProperty("selector")
	private List<Selector> selector;

}
