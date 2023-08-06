/*
 * SPDX-FileCopyrightText: 2006-2021 Istituto Italiano di Tecnologia (IIT)
 * SPDX-License-Identifier: BSD-3-Clause
 */

#include <yarp/dev/INavigation2D.h>
#include <yarp/dev/IMap2D.h>
#include <yarp/dev/Map2DLocation.h>
#include <yarp/dev/Map2DArea.h>
#include <yarp/os/Network.h>
#include <yarp/os/LogStream.h>
#include <yarp/dev/PolyDriver.h>

#include <catch.hpp>
#include <harness.h>

#include "IMap2DTest.h"

using namespace yarp::dev;
using namespace yarp::dev::Nav2D;
using namespace yarp::sig;
using namespace yarp::os;

TEST_CASE("dev::Map2DClientTest", "[yarp::dev]")
{
    YARP_REQUIRE_PLUGIN("map2DServer", "device");
    YARP_REQUIRE_PLUGIN("map2DClient", "device");

    Network::setLocalMode(true);

    SECTION("Checking map2DClient < -> map2DServer communication and yarp::dev::Nav2D::IMap2D methods")
    {
        PolyDriver ddmapserver;
        PolyDriver ddmapclient;
        IMap2D* imap = nullptr;

        ////////"Checking opening map2DServer and map2DClient polydrivers"
        {
            Property pmapserver_cfg;
            pmapserver_cfg.put("device", "map2DServer");
            REQUIRE(ddmapserver.open(pmapserver_cfg));

            Property pmapclient_cfg;
            pmapclient_cfg.put("device", "map2DClient");
            pmapclient_cfg.put("local", "/mapClientTest");
            pmapclient_cfg.put("remote", "/mapServer");
            REQUIRE(ddmapclient.open(pmapclient_cfg));
            REQUIRE(ddmapclient.view(imap));
        }

        //execute tests
        exec_iMap2D_test_1(imap);
        exec_iMap2D_test_2(imap);

        //"Close all polydrivers and check"
        {
            CHECK(ddmapclient.close());
            CHECK(ddmapserver.close());
        }
    }

    Network::setLocalMode(false);
}
