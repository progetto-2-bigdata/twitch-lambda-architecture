package it.uniroma3.bigdata.twitch.dashboard.repository;
import org.springframework.data.cassandra.repository.CassandraRepository;
import org.springframework.data.cassandra.repository.Query;
import org.springframework.stereotype.Repository;

import it.uniroma3.bigdata.twitch.dashboard.domain.*;

import java.util.UUID;


@Repository
public interface DonationRepository extends CassandraRepository<DonationData, UUID> {
	
	@Query("SELECT * FROM AnalyticsKeySpace.Total_Donations WHERE country = ?0 ALLOW FILTERING")
    Iterable<DonationData> findCountry(String country);
}
