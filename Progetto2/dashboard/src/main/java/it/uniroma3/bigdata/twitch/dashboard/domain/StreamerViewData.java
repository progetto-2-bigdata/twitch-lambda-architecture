package it.uniroma3.bigdata.twitch.dashboard.domain;

import org.springframework.data.cassandra.core.cql.PrimaryKeyType;
import org.springframework.data.cassandra.core.mapping.Column;
import org.springframework.data.cassandra.core.mapping.PrimaryKeyColumn;
import org.springframework.data.cassandra.core.mapping.Table;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

@Table("Streamer_Analytics_Views") @Getter @Setter @AllArgsConstructor
public class StreamerViewData {
	
    @PrimaryKeyColumn(name = "streamerID", ordinal = 0, type = PrimaryKeyType.PARTITIONED)
	private String streamerID; 
	
    @PrimaryKeyColumn(name = "hourOfTheDay", ordinal = 1, type = PrimaryKeyType.CLUSTERED)
	private Integer hourOfTheDay; 
    
    @Column(value = "float")
	private Float avgViews; 
  
}
