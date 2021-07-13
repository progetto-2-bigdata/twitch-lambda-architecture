package it.uniroma3.bigdata.twitch.dashboard.repository;

import java.util.UUID;

import org.springframework.data.cassandra.repository.CassandraRepository;
import org.springframework.stereotype.Repository;

import it.uniroma3.bigdata.twitch.dashboard.domain.StreamerFollowerData;

@Repository
public interface StreamerFollowerRepository extends CassandraRepository<StreamerFollowerData, UUID> {}
