package com.mystream.dom;

import com.fasterxml.jackson.annotation.JsonProperty;
import sun.net.www.content.text.plain;

public enum FormatEnum {
	@JsonProperty("text/plain")
	TEXT_PLAIN,
	@JsonProperty("text/html")
	TEXT_HTML,
	@JsonProperty("image/png")
	IMAGE_PNG,
	@JsonProperty("image/jpeg")
	IMAGE_JPEG,
	@JsonProperty("audio/mpeg")
	AUDIO_MPEG;



}
