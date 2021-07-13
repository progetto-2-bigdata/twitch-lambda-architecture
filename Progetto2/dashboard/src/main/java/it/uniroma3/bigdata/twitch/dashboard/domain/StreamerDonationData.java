package it.uniroma3.bigdata.twitch.dashboard.domain;

import java.io.Serializable;

import org.springframework.data.cassandra.core.cql.PrimaryKeyType;
import org.springframework.data.cassandra.core.mapping.Column;
import org.springframework.data.cassandra.core.mapping.PrimaryKeyColumn;
import org.springframework.data.cassandra.core.mapping.Table;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;


@Table("Streamer_Analytics_Donations") @Getter @Setter @AllArgsConstructor
public class StreamerDonationData implements Serializable {
	
	private static final long serialVersionUID = 1L;
	
	@PrimaryKeyColumn(name = "streamerID", ordinal = 0, type = PrimaryKeyType.PARTITIONED)
	private String streamerID; 
	
	@PrimaryKeyColumn(name = "year", ordinal = 1, type = PrimaryKeyType.CLUSTERED)
	private Integer year; 
    
	@PrimaryKeyColumn(name = "month", ordinal = 2, type = PrimaryKeyType.CLUSTERED)
	private Integer month; 
    
    @Column(value = "totalDonations")
	private Long totalDonations; 
}
