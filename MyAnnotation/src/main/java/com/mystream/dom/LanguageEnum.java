package com.mystream.dom;

import com.fasterxml.jackson.annotation.JsonProperty;

public enum LanguageEnum {
	@JsonProperty("en")
	ENGLISH,
	@JsonProperty("tr")
	TURKISH,
	@JsonProperty("de")
	GERMAN,
	@JsonProperty("fr")
	FRENCH,
	@JsonProperty("es")
	SPANISH,
	@JsonProperty("it")
	ITALIAN;


}
