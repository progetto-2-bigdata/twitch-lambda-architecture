package it.uniroma3.bigdata.twitch.dashboard.service;

import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

import it.uniroma3.bigdata.twitch.dashboard.domain.DonationData;
import it.uniroma3.bigdata.twitch.dashboard.domain.StreamerDonationData;
import it.uniroma3.bigdata.twitch.dashboard.domain.StreamerFollowerData;
import it.uniroma3.bigdata.twitch.dashboard.domain.StreamerViewData;
import it.uniroma3.bigdata.twitch.dashboard.repository.DonationRepository;
import it.uniroma3.bigdata.twitch.dashboard.repository.StreamerDonationRepository;
import it.uniroma3.bigdata.twitch.dashboard.repository.StreamerFollowerRepository;
import it.uniroma3.bigdata.twitch.dashboard.repository.StreamerViewRepository;

import org.springframework.messaging.simp.SimpMessagingTemplate;


@Service
public class AnalyticsService {
	
	
	@Autowired
    private SimpMessagingTemplate template;
	
    @Autowired
	private DonationRepository donationRepository; 
	
    @Autowired
	private StreamerDonationRepository streamerDonationRepository; 
	
    @Autowired
	private StreamerFollowerRepository streamerFollowerRepository; 
	
    @Autowired
	private StreamerViewRepository streamerViewRepository; 
    
    @Scheduled(fixedRate = 10000)
    public void send() {
    	List<DonationData> donations = new ArrayList<>(); 
    	List<StreamerDonationData> streamerDonationData = new ArrayList<>(); 
    	List<StreamerFollowerData> streamerFollowerData = new ArrayList<>(); 
    	List<StreamerViewData> streamerViewData = new ArrayList<>(); 
    	
    	this.donationRepository.findAll().forEach(donations::add);
    	this.streamerDonationRepository.findAll().forEach(streamerDonationData::add);
    	this.streamerFollowerRepository.findAll().forEach(streamerFollowerData::add);
    	this.streamerViewRepository.findAll().forEach(streamerViewData::add);
    	
        Response response = new Response();
        response.setDonations(donations);
        response.setStreamerDonations(streamerDonationData);
        response.setStreamerFollower(streamerFollowerData);
        response.setStreamerView(streamerViewData);
        
        this.template.convertAndSend("/topic/realTimeAnalyticsData", response);
    }

}
