package com.mystream.test.repo;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.mystream.dom.Annotation;
import com.mystream.repo.AnnotationRepository;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.orm.jpa.TestEntityManager;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import org.springframework.test.context.junit4.SpringRunner;
import static org.assertj.core.api.Assertions.*;

import java.io.File;
import java.io.IOException;
import java.util.List;

@SpringBootTest
@RunWith(SpringJUnit4ClassRunner.class)
public class AnnotationRepositoryTest {

	@Autowired
	private AnnotationRepository annoRepository;

	@Autowired
	private ObjectMapper objectMapper = new ObjectMapper();

	ClassLoader classLoader = getClass().getClassLoader();

	private void test_save(String testDataFile){
		try{

			File file = new File(classLoader.getResource(testDataFile).getFile());

			Annotation anno = objectMapper.readValue(file, Annotation.class);
			annoRepository.save(anno);

			Annotation foundAnno = annoRepository.findByCanonical(anno.getCanonical());

			assertThat(foundAnno != null );
			assertThat(foundAnno.getCanonical() == anno.getCanonical() );
			assertThat(foundAnno.getBody() != null );
			assertThat(foundAnno.getTarget() != null );

			annoRepository.delete(foundAnno);

		}catch (Exception ex){
			System.out.println(ex.getMessage());
		}
	}

	@Test
	public void test_save_imageTarget() {

		test_save("test_save_imageTarget.json");

	}

	@Test
	public void test_save_textTarget() {

		test_save("test_save_textTarget.json");

	}

	@Test
	public void test_save_bodyWithVideo() {

		test_save("test_save_bodyWithVideo.json");

	}

	@Test
	public void test_save_bodyWithImage() {

		test_save("test_save_bodyWithImage.json");

	}

	@Test
	public void test_save_bodyWithText() {

		test_save("test_save_bodyWithText.json");

	}

	@Test
	public void test_findByTarget_SourceLike() {

		String test_source = "localhost:8080";
		List<Annotation> annoList = annoRepository.findByTarget_SourceLike(test_source);

		assertThat(annoList != null );
		assertThat(annoList.size() > 0);

		for ( Annotation anno : annoList ) {
			assertThat(anno.getBody() != null );
			assertThat( anno.getTarget() != null );
		}


	}



}