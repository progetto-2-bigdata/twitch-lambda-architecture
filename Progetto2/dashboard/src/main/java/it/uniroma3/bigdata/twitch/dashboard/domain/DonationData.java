package it.uniroma3.bigdata.twitch.dashboard.domain;

import java.io.Serializable;

import org.springframework.data.cassandra.core.cql.PrimaryKeyType;
import org.springframework.data.cassandra.core.mapping.Column;
import org.springframework.data.cassandra.core.mapping.PrimaryKeyColumn;
import org.springframework.data.cassandra.core.mapping.Table;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;


@Table("Total_Donations") @Getter @Setter @AllArgsConstructor @NoArgsConstructor
public class DonationData implements Serializable {
	
	private static final long serialVersionUID = 1L;

	@PrimaryKeyColumn(name = "hourOfTheDay", ordinal = 0, type = PrimaryKeyType.PARTITIONED)
	private Integer hourOfTheDay;  
	
    @PrimaryKeyColumn(name = "dayOfTheWeek", ordinal = 1, type = PrimaryKeyType.CLUSTERED)
	private Integer dayOfTheWeek; 
	
    @PrimaryKeyColumn(name = "country", ordinal = 2, type = PrimaryKeyType.CLUSTERED)
	private String country; 
	
    @Column(value = "totalDonations")
	private Integer totalDonations; 

}
