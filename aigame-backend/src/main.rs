// ************************************************************************** //
//                                                                            //
//                                                        :::      ::::::::   //
//   main.rs                                            :+:      :+:    :+:   //
//                                                    +:+ +:+         +:+     //
//   By: dfine <coding@dfine.tech>                  +#+  +:+       +#+        //
//                                                +#+#+#+#+#+   +#+           //
//   Created: 2025/03/20 20:09:17 by dfine             #+#    #+#             //
//   Updated: 2025/03/20 20:11:07 by dfine            ###   ########.fr       //
//                                                                            //
// ************************************************************************** //

mod db;
mod logger;
mod routes;
mod scheme;
mod utils;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let _guard = logger::init().await;
    routes::create_routes().await
}
