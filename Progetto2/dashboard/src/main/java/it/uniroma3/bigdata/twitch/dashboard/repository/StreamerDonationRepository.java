package it.uniroma3.bigdata.twitch.dashboard.repository;

import java.util.UUID;

import org.springframework.data.cassandra.repository.CassandraRepository;
import org.springframework.stereotype.Repository;

import it.uniroma3.bigdata.twitch.dashboard.domain.StreamerDonationData;

@Repository
public interface StreamerDonationRepository extends CassandraRepository<StreamerDonationData, UUID> {}
