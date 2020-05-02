package com.mystream.dom.selector;

import com.fasterxml.jackson.annotation.JsonTypeName;
import lombok.Getter;
import lombok.Setter;
@JsonTypeName("FragmentSelector")
public class FragmentSelector extends Selector {

	@Getter
	@Setter
	private String value;

	@Getter
	@Setter
	private String conformsTo;
}
