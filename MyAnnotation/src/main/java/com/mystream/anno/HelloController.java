package com.mystream.anno;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HelloController {

	@RequestMapping("/helloAnnotation")
	public String hello(){
		return "Hello W3C Annotation World!";
	}
}
