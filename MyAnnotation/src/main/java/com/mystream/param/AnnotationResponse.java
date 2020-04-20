package com.mystream.param;

import lombok.Setter;

import java.util.HashMap;

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
