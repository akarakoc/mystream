package com.mystream.dom;

import sun.net.www.content.text.plain;

public enum FormatEnum {

	TEXT_PLAIN("text/plain");


	FormatEnum(String value) {
		this.value = value;
	}

	private final String value;

	public String getValue() {
		return this.value;
	}
}
