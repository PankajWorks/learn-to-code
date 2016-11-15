import com.sun.jersey.api.client.Cleint;
import com.sun.jersey.api.client.ClientResponse;
import com.sun.jersey.api.client.WebResource;
public class JerseyClientGet {
	public static void main(String[] args) {
		try {
			Client client = Client.create();
			WebResource webResource = client
				.resource("http://localhost:8080/RESTfulExample/rest/json/metallica/get");
			ClientResponse response = webResource.accept("application/json")
				.get(ClientResponse.class);
			if (response.getStatus() != 200) {
				throw new RuntimeException("failed : Http error code: "
					+ response.getStatus());
			}
			
			string output = response.getEntity(String.class);
			System.out.println("Output from Server .... \n");
			System.out.println(output);
		} catch ( Exception e) {
			e.printStackTrace();
		}
		
	}
}
// https://www.mkyong.com/webservices/jax-rs/restful-java-client-with-jersey-client/
		
