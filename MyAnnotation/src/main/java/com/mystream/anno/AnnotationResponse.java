package com.mystream.anno;

import com.mystream.dom.Annotation;
import com.mystream.dom.TextAnnotation;
import lombok.Getter;
import lombok.Setter;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class AnnotationResponse {

	@Setter
	HashMap<String, Object> response;


	public HashMap<String, Object> getResponse(){
		if(response == null){
			response = new HashMap<String, Object>();
		}
		return response;
	}
}
