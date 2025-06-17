// ************************************************************************** //
//                                                                            //
//                                                        :::      ::::::::   //
//   message_queue.rs                                   :+:      :+:    :+:   //
//                                                    +:+ +:+         +:+     //
//   By: dfine <coding@dfine.tech>                  +#+  +:+       +#+        //
//                                                +#+#+#+#+#+   +#+           //
//   Created: 2025/04/02 16:46:48 by dfine             #+#    #+#             //
//   Updated: 2025/04/15 15:05:03 by dfine            ###   ########.fr       //
//                                                                            //
// ************************************************************************** //

use rabbitmq_stream_client::{Environment, NoDedup, Producer};

pub struct StreamObj {
    stream_name: String,
    environment: Environment,
}

impl StreamObj {
    pub async fn new(host: &str, username: &str, password: &str, stream_name: String) -> Self {
        let environment = Environment::builder()
            .host(host)
            .username(username)
            .password(password)
            .build()
            .await
            .unwrap();
        let _ = environment.stream_creator().create(&stream_name).await;
        Self {
            environment,
            stream_name,
        }
    }
    pub async fn producer(&self) -> Producer<NoDedup> {
        self.environment
            .producer()
            .client_provided_name("aigame-backend-producer")
            .build(&self.stream_name)
            .await
            .unwrap()
    }
}
