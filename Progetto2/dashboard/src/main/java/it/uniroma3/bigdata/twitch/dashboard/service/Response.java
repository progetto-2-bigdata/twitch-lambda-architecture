package it.uniroma3.bigdata.twitch.dashboard.service;

import java.io.Serializable;
import java.util.List;

import it.uniroma3.bigdata.twitch.dashboard.domain.DonationData;
import it.uniroma3.bigdata.twitch.dashboard.domain.StreamerDonationData;
import it.uniroma3.bigdata.twitch.dashboard.domain.StreamerFollowerData;
import it.uniroma3.bigdata.twitch.dashboard.domain.StreamerViewData;
import lombok.Getter;
import lombok.Setter;


@Getter @Setter
public class Response implements Serializable {
	
	
	private static final long serialVersionUID = 1L;
	
	private List<DonationData> donations; 
	
	private List<StreamerDonationData> streamerDonations; 
	
	private List<StreamerFollowerData> streamerFollower; 

	private List<StreamerViewData> streamerView; 


}
