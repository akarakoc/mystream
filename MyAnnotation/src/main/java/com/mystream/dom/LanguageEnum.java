package com.mystream.dom;

public enum LanguageEnum {

	ENGLISH("en"),
	TURKISH("tr"),
	GERMAN("de");


	LanguageEnum(String value) {
		this.value = value;
	}

	private final String value;

	public String getValue() {
		return this.value;
	}
}
